"""REST API routes for algorithms and related resources."""

from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.resources.views import ResourceViewSet

from .views import AlgorithmViewSet, CategoryListAPIView, CommentViewSet, RatingViewSet

router = DefaultRouter()
router.register("algorithms", AlgorithmViewSet, basename="api-algorithm")
router.register("resources", ResourceViewSet, basename="api-resource")
router.register("comments", CommentViewSet, basename="api-comment")
router.register("ratings", RatingViewSet, basename="api-rating")

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="api-categories"),
]

urlpatterns += router.urls
