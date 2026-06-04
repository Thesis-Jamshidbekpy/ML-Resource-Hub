"""Admin registration for account-related models."""

from django.contrib import admin

from .models import FavoriteAlgorithm, Profile, RecentlyViewedAlgorithm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Support profile search and quick moderation in the admin panel."""

    list_display = ("user", "institution", "academic_interest", "updated_at")
    search_fields = ("user__username", "user__email", "institution", "academic_interest")
    list_select_related = ("user",)


@admin.register(FavoriteAlgorithm)
class FavoriteAlgorithmAdmin(admin.ModelAdmin):
    """Manage the favorite relationships used by the frontend."""

    list_display = ("user", "algorithm", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "algorithm__name")
    autocomplete_fields = ("user", "algorithm")


@admin.register(RecentlyViewedAlgorithm)
class RecentlyViewedAlgorithmAdmin(admin.ModelAdmin):
    """Inspect user browsing behavior for academic demonstrations."""

    list_display = ("user", "algorithm", "last_viewed_at")
    list_filter = ("last_viewed_at",)
    search_fields = ("user__username", "algorithm__name")
    autocomplete_fields = ("user", "algorithm")
