"""Database models for user profiles and personalized collections."""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """Extend Django's built-in user model with academic profile metadata."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(blank=True, verbose_name=_("Bio"))
    avatar = models.ImageField(upload_to="profiles/avatars/", blank=True, null=True, verbose_name=_("Avatar"))
    institution = models.CharField(max_length=255, blank=True, verbose_name=_("Institution"))
    academic_interest = models.CharField(max_length=255, blank=True, verbose_name=_("Academic interest"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ["user__username"]

    def __str__(self) -> str:
        return f"{self.user.username} profile"

    def get_absolute_url(self) -> str:
        return reverse("accounts:profile")


class FavoriteAlgorithm(models.Model):
    """Store user-algorithm favorite relationships."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_algorithms",
    )
    algorithm = models.ForeignKey(
        "algorithms.Algorithm",
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("Favorite")
        verbose_name_plural = _("Favorites")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "algorithm"],
                name="unique_favorite_algorithm_per_user",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.algorithm.name}"


class RecentlyViewedAlgorithm(models.Model):
    """Track the latest algorithms visited by each authenticated user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recently_viewed_algorithms",
    )
    algorithm = models.ForeignKey(
        "algorithms.Algorithm",
        on_delete=models.CASCADE,
        related_name="recent_views",
    )
    last_viewed_at = models.DateTimeField(auto_now=True, verbose_name=_("Last viewed at"))

    class Meta:
        verbose_name = _("Recent view")
        verbose_name_plural = _("Recent views")
        ordering = ["-last_viewed_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "algorithm"],
                name="unique_recent_algorithm_per_user",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} recently viewed {self.algorithm.name}"
