"""URL routes for algorithm browsing and interaction."""

from django.urls import path

from .views import (
    AlgorithmDetailView,
    AlgorithmListView,
    CommentCreateView,
    FavoriteToggleView,
    RatingUpsertView,
)

app_name = "algorithms"

urlpatterns = [
    path("", AlgorithmListView.as_view(), name="list"),
    path("<slug:slug>/", AlgorithmDetailView.as_view(), name="detail"),
    path("<slug:slug>/comment/", CommentCreateView.as_view(), name="comment"),
    path("<slug:slug>/rate/", RatingUpsertView.as_view(), name="rate"),
    path("<slug:slug>/favorite/", FavoriteToggleView.as_view(), name="favorite"),
]
