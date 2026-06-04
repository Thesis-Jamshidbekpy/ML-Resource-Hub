"""URL routes for the homepage, dashboard, and unified search."""

from django.urls import path

from .views import DashboardView, HomeView, SearchResultsView

app_name = "dashboard"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("search/", SearchResultsView.as_view(), name="search_results"),
]
