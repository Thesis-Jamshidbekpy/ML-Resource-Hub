"""Admin configuration for learning resources and bookmarks."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Resource, ResourceBookmark


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Offer searchable resource management for curated learning content."""

    list_display = ("title", "title_uz", "algorithm", "resource_type", "author", "download_count", "created_at")
    list_filter = ("resource_type", "created_at")
    search_fields = (
        "title",
        "title_uz",
        "author",
        "author_uz",
        "description",
        "description_uz",
        "algorithm__name",
        "algorithm__name_uz",
    )
    autocomplete_fields = ("algorithm",)
    fieldsets = (
        (_("Primary Information"), {"fields": ("algorithm", "resource_type", "external_url", "file")}),
        (_("English Content"), {"fields": ("title", "author", "description")}),
        (_("Uzbek Content"), {"fields": ("title_uz", "author_uz", "description_uz")}),
        (_("Analytics"), {"fields": ("download_count", "created_at")}),
    )
    readonly_fields = ("download_count", "created_at")


@admin.register(ResourceBookmark)
class ResourceBookmarkAdmin(admin.ModelAdmin):
    """Manage bookmarked resources for user study collections."""

    list_display = ("user", "resource", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "resource__title", "resource__title_uz")
    autocomplete_fields = ("user", "resource")
