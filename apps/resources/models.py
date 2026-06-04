"""Database models for educational materials linked to algorithms."""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import get_language, gettext_lazy as _


class ResourceType(models.TextChoices):
    """Controlled vocabulary for resource discovery and filtering."""

    BOOK = "book", _("Book")
    ARTICLE = "article", _("Article")
    RESEARCH_PAPER = "research_paper", _("Research Paper")
    VIDEO = "video", _("Video")
    DOCUMENTATION = "documentation", _("Documentation")
    DATASET = "dataset", _("Dataset")


class Resource(models.Model):
    """Represent a learning resource associated with an algorithm."""

    algorithm = models.ForeignKey(
        "algorithms.Algorithm",
        on_delete=models.CASCADE,
        related_name="resources",
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    title_uz = models.CharField(max_length=255, blank=True, verbose_name=_("Title (Uzbek)"))
    resource_type = models.CharField(max_length=32, choices=ResourceType.choices, verbose_name=_("Resource type"))
    author = models.CharField(max_length=255, blank=True, verbose_name=_("Author"))
    author_uz = models.CharField(max_length=255, blank=True, verbose_name=_("Author (Uzbek)"))
    description = models.TextField(verbose_name=_("Description"))
    description_uz = models.TextField(blank=True, verbose_name=_("Description (Uzbek)"))
    external_url = models.URLField(blank=True, verbose_name=_("External URL"))
    file = models.FileField(upload_to="resources/files/", blank=True, null=True, verbose_name=_("File"))
    download_count = models.PositiveIntegerField(default=0, verbose_name=_("Download count"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("Resource")
        verbose_name_plural = _("Resources")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["resource_type"]),
            models.Index(fields=["-created_at"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("resources:detail", kwargs={"pk": self.pk})

    def _localized_value(self, base_field: str, uzbek_field: str) -> str:
        """Return Uzbek content when active, otherwise the English field."""

        language = (get_language() or "en").split("-")[0]
        if language == "uz":
            translated = getattr(self, uzbek_field, "")
            if translated:
                return translated
        return getattr(self, base_field)

    @property
    def localized_title(self) -> str:
        return self._localized_value("title", "title_uz")

    @property
    def localized_author(self) -> str:
        return self._localized_value("author", "author_uz")

    @property
    def localized_description(self) -> str:
        return self._localized_value("description", "description_uz")


class ResourceBookmark(models.Model):
    """Allow users to bookmark high-value resources for later review."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resource_bookmarks",
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="bookmarked_by",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("Bookmark")
        verbose_name_plural = _("Bookmarks")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "resource"],
                name="unique_resource_bookmark_per_user",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} bookmarked {self.resource.title}"
