"""Views for the landing page, dashboard, and cross-domain search."""

from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView

from apps.algorithms.models import Algorithm, AlgorithmCategory
from apps.resources.models import Resource, ResourceType

from .forms import GlobalSearchForm


class HomeView(TemplateView):
    """Render the project homepage with featured content highlights."""

    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_algorithms"] = (
            Algorithm.objects.annotate(
                average_rating=Coalesce(Avg("ratings__score"), 0.0),
                ratings_count=Count("ratings", distinct=True),
            )
            .order_by("-view_count", "name")[:6]
        )
        context["latest_resources"] = Resource.objects.select_related("algorithm").order_by("-created_at")[:6]
        context["search_form"] = GlobalSearchForm(self.request.GET or None)
        if self.request.user.is_authenticated:
            context["recently_viewed"] = (
                self.request.user.recently_viewed_algorithms.select_related("algorithm")
                .all()
                .order_by("-last_viewed_at")[:6]
            )
        return context


class DashboardView(TemplateView):
    """Display platform-level analytics and recently added content."""

    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_algorithms"] = Algorithm.objects.count()
        context["total_resources"] = Resource.objects.count()
        context["total_users"] = User.objects.count()
        context["most_viewed_algorithms"] = Algorithm.objects.order_by("-view_count", "name")[:5]
        context["latest_resources"] = Resource.objects.select_related("algorithm").order_by("-created_at")[:8]
        return context


class SearchResultsView(TemplateView):
    """Combine algorithm and resource discovery in one unified result page."""

    template_name = "dashboard/search_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()
        resource_type = self.request.GET.get("resource_type", "").strip()

        algorithms = Algorithm.objects.annotate(
            average_rating=Coalesce(Avg("ratings__score"), 0.0),
            ratings_count=Count("ratings", distinct=True),
        )
        resources = Resource.objects.select_related("algorithm")

        if query:
            algorithms = algorithms.filter(Q(name__icontains=query) | Q(name_uz__icontains=query))
            resources = resources.filter(Q(title__icontains=query) | Q(title_uz__icontains=query))
        if category:
            algorithms = algorithms.filter(category=category)
        if resource_type:
            resources = resources.filter(resource_type=resource_type)

        context["query"] = query
        context["algorithms"] = algorithms.order_by("name")[:20]
        context["resources"] = resources.order_by("-created_at")[:20]
        context["search_form"] = GlobalSearchForm(self.request.GET or None)
        context["selected_category"] = category
        context["selected_resource_type"] = resource_type
        context["category_choices"] = AlgorithmCategory.choices
        context["resource_type_choices"] = ResourceType.choices
        return context
