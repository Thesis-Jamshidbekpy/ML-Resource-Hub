"""Views for resource browsing, bookmarking, downloads, and the API."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView, ListView
from rest_framework import permissions, viewsets

from .forms import ResourceFilterForm
from .models import Resource, ResourceBookmark
from .serializers import ResourceSerializer


class ResourceListView(ListView):
    """Browse learning resources with search and type-based filters."""

    model = Resource
    template_name = "resources/resource_list.html"
    context_object_name = "resources"
    paginate_by = 9

    def get_queryset(self):
        queryset = Resource.objects.select_related("algorithm")
        search_query = self.request.GET.get("q", "").strip()
        resource_type = self.request.GET.get("resource_type", "").strip()
        ordering = self.request.GET.get("ordering", "date")

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(title_uz__icontains=search_query))
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)

        if ordering == "popularity":
            queryset = queryset.order_by("-download_count", "title")
        elif ordering == "title":
            queryset = queryset.order_by("title")
        else:
            queryset = queryset.order_by("-created_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = ResourceFilterForm(self.request.GET or None)
        return context


class ResourceDetailView(DetailView):
    """Show full metadata and access options for one learning resource."""

    model = Resource
    template_name = "resources/resource_detail.html"
    context_object_name = "resource"

    def get_queryset(self):
        return Resource.objects.select_related("algorithm")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_bookmarked"] = False
        if self.request.user.is_authenticated:
            context["is_bookmarked"] = ResourceBookmark.objects.filter(
                user=self.request.user,
                resource=self.object,
            ).exists()
        return context


class ResourceBookmarkToggleView(LoginRequiredMixin, View):
    """Add or remove a resource from the current user's bookmarks."""

    def post(self, request, pk):
        resource = get_object_or_404(Resource, pk=pk)
        bookmark, created = ResourceBookmark.objects.get_or_create(
            user=request.user,
            resource=resource,
        )
        if created:
            messages.success(request, _("Resource bookmarked successfully."))
        else:
            bookmark.delete()
            messages.info(request, _("Resource removed from your bookmarks."))
        return redirect(resource.get_absolute_url())


class ResourceDownloadView(View):
    """Increment the download counter before serving or redirecting."""

    def get(self, request, pk):
        resource = get_object_or_404(Resource, pk=pk)
        Resource.objects.filter(pk=resource.pk).update(download_count=F("download_count") + 1)

        if resource.file:
            if not resource.file.storage.exists(resource.file.name):
                raise Http404(_("The requested file could not be found."))
            return FileResponse(resource.file.open("rb"), as_attachment=True)

        if resource.external_url:
            return redirect(resource.external_url)

        messages.error(request, _("This resource does not have a downloadable file or external link."))
        return redirect(resource.get_absolute_url())


class ResourceViewSet(viewsets.ModelViewSet):
    """REST endpoint for browsing and managing resource records."""

    queryset = Resource.objects.select_related("algorithm")
    serializer_class = ResourceSerializer
    search_fields = ("title", "title_uz", "description", "description_uz", "author", "author_uz")
    filterset_fields = ("resource_type", "algorithm")
    ordering_fields = ("title", "created_at", "download_count")

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
