"""Views for algorithm browsing, interaction, and REST APIs."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, F, Prefetch, Q
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView, ListView
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import FavoriteAlgorithm, RecentlyViewedAlgorithm

from .forms import AlgorithmFilterForm, CommentForm, RatingForm
from .models import Algorithm, AlgorithmCategory, Comment, Rating
from .serializers import (
    AlgorithmSerializer,
    CategorySerializer,
    CommentSerializer,
    RatingSerializer,
)


class OwnerOrReadOnly(permissions.BasePermission):
    """Allow unsafe requests only to record owners or administrators."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (obj.user == request.user or request.user.is_staff)


class AlgorithmListView(ListView):
    """Browse algorithm records with search, filter, and ordering controls."""

    model = Algorithm
    template_name = "algorithms/algorithm_list.html"
    context_object_name = "algorithms"
    paginate_by = 9

    def get_queryset(self):
        queryset = Algorithm.objects.annotate(
            average_rating=Coalesce(Avg("ratings__score"), 0.0),
            ratings_count=Count("ratings", distinct=True),
            favorites_count=Count("favorited_by", distinct=True),
        )
        search_query = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()
        ordering = self.request.GET.get("ordering", "name")

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(name_uz__icontains=search_query))
        if category:
            queryset = queryset.filter(category=category)

        if ordering == "popularity":
            queryset = queryset.order_by("-view_count", "-favorites_count", "-ratings_count", "name")
        elif ordering == "date":
            queryset = queryset.order_by("-created_at")
        else:
            queryset = queryset.order_by("name")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = AlgorithmFilterForm(self.request.GET or None)
        return context


class AlgorithmDetailView(DetailView):
    """Present the academic profile, discussion, and resources for one algorithm."""

    model = Algorithm
    template_name = "algorithms/algorithm_detail.html"
    context_object_name = "algorithm"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            Algorithm.objects.annotate(
                average_rating=Coalesce(Avg("ratings__score"), 0.0),
                ratings_count=Count("ratings", distinct=True),
            )
            .prefetch_related(
                Prefetch("comments", queryset=Comment.objects.select_related("user")),
                "resources",
            )
        )

    def get_object(self, queryset=None):
        algorithm = super().get_object(queryset)
        Algorithm.objects.filter(pk=algorithm.pk).update(view_count=F("view_count") + 1)
        algorithm.refresh_from_db(fields=["view_count"])
        if self.request.user.is_authenticated:
            RecentlyViewedAlgorithm.objects.update_or_create(
                user=self.request.user,
                algorithm=algorithm,
            )
        return algorithm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        algorithm = self.object
        user_rating = None
        is_favorited = False
        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(user=self.request.user, algorithm=algorithm).first()
            is_favorited = FavoriteAlgorithm.objects.filter(
                user=self.request.user,
                algorithm=algorithm,
            ).exists()
        context["comment_form"] = CommentForm()
        context["rating_form"] = RatingForm(instance=user_rating)
        context["related_algorithms"] = (
            Algorithm.objects.filter(category=algorithm.category)
            .exclude(pk=algorithm.pk)
            .order_by("-view_count", "name")[:4]
        )
        context["is_favorited"] = is_favorited
        return context


class CommentCreateView(LoginRequiredMixin, View):
    """Create a new comment for an algorithm detail page."""

    def post(self, request, slug):
        algorithm = get_object_or_404(Algorithm, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.algorithm = algorithm
            comment.save()
            messages.success(request, _("Your comment has been published."))
        else:
            messages.error(request, _("Comment submission failed. Please try again."))
        return redirect(algorithm.get_absolute_url())


class RatingUpsertView(LoginRequiredMixin, View):
    """Create or update a user's rating for the current algorithm."""

    def post(self, request, slug):
        algorithm = get_object_or_404(Algorithm, slug=slug)
        existing_rating = Rating.objects.filter(user=request.user, algorithm=algorithm).first()
        form = RatingForm(request.POST, instance=existing_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.algorithm = algorithm
            rating.save()
            messages.success(request, _("Your rating has been saved."))
        else:
            messages.error(request, _("Rating submission failed. Please select a score from 1 to 5."))
        return redirect(algorithm.get_absolute_url())


class FavoriteToggleView(LoginRequiredMixin, View):
    """Add or remove an algorithm from the current user's favorites."""

    def post(self, request, slug):
        algorithm = get_object_or_404(Algorithm, slug=slug)
        favorite, created = FavoriteAlgorithm.objects.get_or_create(
            user=request.user,
            algorithm=algorithm,
        )
        if created:
            messages.success(request, _("%(algorithm)s was added to your favorites.") % {"algorithm": algorithm.localized_name})
        else:
            favorite.delete()
            messages.info(request, _("%(algorithm)s was removed from your favorites.") % {"algorithm": algorithm.localized_name})
        return redirect(algorithm.get_absolute_url())


class AlgorithmViewSet(viewsets.ModelViewSet):
    """REST endpoint for browsing and managing algorithms."""

    queryset = (
        Algorithm.objects.annotate(
            average_rating=Coalesce(Avg("ratings__score"), 0.0),
            ratings_count=Count("ratings", distinct=True),
        )
        .order_by("name")
    )
    serializer_class = AlgorithmSerializer
    search_fields = ("name", "name_uz", "description", "description_uz", "algorithm_type", "algorithm_type_uz")
    filterset_fields = ("category",)
    ordering_fields = ("name", "created_at", "view_count")

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class CategoryListAPIView(APIView):
    """Return the available algorithm categories for API consumers."""

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = CategorySerializer(CategorySerializer.from_choices(), many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """REST endpoint for retrieving and posting algorithm comments."""

    queryset = Comment.objects.select_related("user", "algorithm")
    serializer_class = CommentSerializer
    filterset_fields = ("algorithm", "user")
    ordering_fields = ("created_at",)

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [permissions.IsAuthenticated(), OwnerOrReadOnly()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RatingViewSet(viewsets.ModelViewSet):
    """REST endpoint for retrieving and managing algorithm ratings."""

    queryset = Rating.objects.select_related("user", "algorithm")
    serializer_class = RatingSerializer
    filterset_fields = ("algorithm", "user", "score")
    ordering_fields = ("created_at", "updated_at", "score")

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [permissions.IsAuthenticated(), OwnerOrReadOnly()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
