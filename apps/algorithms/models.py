"""Domain models describing machine learning algorithms and discussion."""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import get_language, gettext_lazy as _


class AlgorithmCategory(models.TextChoices):
    """Controlled vocabulary for major machine learning categories."""

    REGRESSION = "regression", _("Regression")
    CLASSIFICATION = "classification", _("Classification")
    CLUSTERING = "clustering", _("Clustering")
    DEEP_LEARNING = "deep_learning", _("Deep Learning")
    REINFORCEMENT_LEARNING = "reinforcement_learning", _("Reinforcement Learning")
    DIMENSIONALITY_REDUCTION = "dimensionality_reduction", _("Dimensionality Reduction")
    ENSEMBLE_LEARNING = "ensemble_learning", _("Ensemble Learning")


class Algorithm(models.Model):
    """Represent a machine learning algorithm and its academic profile."""

    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    name_uz = models.CharField(max_length=255, blank=True, verbose_name=_("Name (Uzbek)"))
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_("Slug"))
    category = models.CharField(max_length=64, choices=AlgorithmCategory.choices, verbose_name=_("Category"))
    algorithm_type = models.CharField(max_length=255, verbose_name=_("Algorithm type"))
    algorithm_type_uz = models.CharField(max_length=255, blank=True, verbose_name=_("Algorithm type (Uzbek)"))
    description = models.TextField(verbose_name=_("Description"))
    description_uz = models.TextField(blank=True, verbose_name=_("Description (Uzbek)"))
    mathematical_foundation = models.TextField(verbose_name=_("Mathematical foundation"))
    mathematical_foundation_uz = models.TextField(blank=True, verbose_name=_("Mathematical foundation (Uzbek)"))
    advantages = models.TextField(verbose_name=_("Advantages"))
    advantages_uz = models.TextField(blank=True, verbose_name=_("Advantages (Uzbek)"))
    disadvantages = models.TextField(verbose_name=_("Disadvantages"))
    disadvantages_uz = models.TextField(blank=True, verbose_name=_("Disadvantages (Uzbek)"))
    applications = models.TextField(verbose_name=_("Applications"))
    applications_uz = models.TextField(blank=True, verbose_name=_("Applications (Uzbek)"))
    complexity = models.CharField(max_length=255, verbose_name=_("Complexity"))
    complexity_uz = models.CharField(max_length=255, blank=True, verbose_name=_("Complexity (Uzbek)"))
    image = models.ImageField(upload_to="algorithms/images/", blank=True, null=True, verbose_name=_("Image"))
    view_count = models.PositiveIntegerField(default=0, verbose_name=_("View count"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Algorithm")
        verbose_name_plural = _("Algorithms")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
            models.Index(fields=["-created_at"]),
            models.Index(fields=["-view_count"]),
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("algorithms:detail", kwargs={"slug": self.slug})

    def _localized_value(self, base_field: str, uzbek_field: str) -> str:
        """Return the localized field value with graceful fallback to English."""

        language = (get_language() or "en").split("-")[0]
        if language == "uz":
            translated = getattr(self, uzbek_field, "")
            if translated:
                return translated
        return getattr(self, base_field)

    @property
    def localized_name(self) -> str:
        return self._localized_value("name", "name_uz")

    @property
    def localized_algorithm_type(self) -> str:
        return self._localized_value("algorithm_type", "algorithm_type_uz")

    @property
    def localized_description(self) -> str:
        return self._localized_value("description", "description_uz")

    @property
    def localized_mathematical_foundation(self) -> str:
        return self._localized_value("mathematical_foundation", "mathematical_foundation_uz")

    @property
    def localized_advantages(self) -> str:
        return self._localized_value("advantages", "advantages_uz")

    @property
    def localized_disadvantages(self) -> str:
        return self._localized_value("disadvantages", "disadvantages_uz")

    @property
    def localized_applications(self) -> str:
        return self._localized_value("applications", "applications_uz")

    @property
    def localized_complexity(self) -> str:
        return self._localized_value("complexity", "complexity_uz")


class Comment(models.Model):
    """Store narrative feedback and discussion for a given algorithm."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="algorithm_comments",
    )
    algorithm = models.ForeignKey(
        Algorithm,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField(verbose_name=_("Text"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return f"Comment by {self.user.username} on {self.algorithm.name}"


class Rating(models.Model):
    """Store numeric algorithm evaluations on a five-point scale."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="algorithm_ratings",
    )
    algorithm = models.ForeignKey(
        Algorithm,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Score"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "algorithm"],
                name="unique_algorithm_rating_per_user",
            )
        ]

    def __str__(self) -> str:
        return f"{self.algorithm.name} rated {self.score} by {self.user.username}"
