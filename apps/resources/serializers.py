"""Serializers for educational resources and bookmarks."""

from rest_framework import serializers

from .models import Resource, ResourceBookmark


class ResourceSerializer(serializers.ModelSerializer):
    """Serialize resource data for public API consumers."""

    algorithm_name = serializers.CharField(source="algorithm.name", read_only=True)
    resource_type_display = serializers.CharField(source="get_resource_type_display", read_only=True)
    localized_title = serializers.CharField(read_only=True)
    localized_author = serializers.CharField(read_only=True)
    localized_description = serializers.CharField(read_only=True)

    class Meta:
        model = Resource
        fields = (
            "id",
            "algorithm",
            "algorithm_name",
            "title",
            "title_uz",
            "localized_title",
            "resource_type",
            "resource_type_display",
            "author",
            "author_uz",
            "localized_author",
            "description",
            "description_uz",
            "localized_description",
            "external_url",
            "file",
            "download_count",
            "created_at",
        )


class ResourceBookmarkSerializer(serializers.ModelSerializer):
    """Serialize bookmark relationships when needed internally."""

    class Meta:
        model = ResourceBookmark
        fields = ("id", "user", "resource", "created_at")
