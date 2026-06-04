"""URL routes for resource discovery and bookmarking."""

from django.urls import path

from .views import (
    ResourceBookmarkToggleView,
    ResourceDetailView,
    ResourceDownloadView,
    ResourceListView,
)

app_name = "resources"

urlpatterns = [
    path("", ResourceListView.as_view(), name="list"),
    path("<int:pk>/", ResourceDetailView.as_view(), name="detail"),
    path("<int:pk>/bookmark/", ResourceBookmarkToggleView.as_view(), name="bookmark"),
    path("<int:pk>/download/", ResourceDownloadView.as_view(), name="download"),
]
