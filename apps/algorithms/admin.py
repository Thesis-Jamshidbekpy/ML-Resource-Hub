"""Admin configuration for algorithms, comments, and ratings."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.resources.models import Resource

from .models import Algorithm, Comment, Rating


class ResourceInline(admin.TabularInline):
    """Show linked learning resources directly from the algorithm admin."""

    model = Resource
    extra = 0
    fields = ("title", "title_uz", "resource_type", "author", "author_uz", "download_count", "created_at")
    readonly_fields = ("download_count", "created_at")


class CommentInline(admin.TabularInline):
    """Surface algorithm discussion without leaving the parent record."""

    model = Comment
    extra = 0
    fields = ("user", "text", "created_at")
    readonly_fields = ("created_at",)


class RatingInline(admin.TabularInline):
    """Show individual algorithm scores inline for moderation."""

    model = Rating
    extra = 0
    fields = ("user", "score", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    """Provide a feature-rich admin panel for algorithm curation."""

    list_display = ("name", "name_uz", "category", "algorithm_type", "view_count", "created_at", "updated_at")
    list_filter = ("category", "created_at", "updated_at")
    search_fields = (
        "name",
        "name_uz",
        "algorithm_type",
        "algorithm_type_uz",
        "description",
        "description_uz",
        "applications",
        "applications_uz",
    )
    prepopulated_fields = {"slug": ("name",)}
    inlines = (ResourceInline, CommentInline, RatingInline)
    ordering = ("name",)
    fieldsets = (
        (_("Primary Information"), {"fields": ("name", "name_uz", "slug", "category", "image")}),
        (_("Classification"), {"fields": ("algorithm_type", "algorithm_type_uz", "complexity", "complexity_uz")}),
        (_("English Content"), {"fields": ("description", "mathematical_foundation", "advantages", "disadvantages", "applications")}),
        (_("Uzbek Content"), {"fields": ("description_uz", "mathematical_foundation_uz", "advantages_uz", "disadvantages_uz", "applications_uz")}),
        (_("Analytics"), {"fields": ("view_count", "created_at", "updated_at")}),
    )
    readonly_fields = ("view_count", "created_at", "updated_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Enable moderation and filtering of user-submitted comments."""

    list_display = ("algorithm", "user", "created_at")
    list_filter = ("created_at", "algorithm")
    search_fields = ("algorithm__name", "algorithm__name_uz", "user__username", "text")
    autocomplete_fields = ("user", "algorithm")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Inspect numeric ratings and their authors."""

    list_display = ("algorithm", "user", "score", "updated_at")
    list_filter = ("score", "updated_at")
    search_fields = ("algorithm__name", "algorithm__name_uz", "user__username")
    autocomplete_fields = ("user", "algorithm")
