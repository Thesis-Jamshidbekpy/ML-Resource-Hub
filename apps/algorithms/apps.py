"""Application configuration for algorithm resources."""

from django.apps import AppConfig


class AlgorithmsConfig(AppConfig):
    """Declare metadata for the algorithms app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.algorithms"
    label = "algorithms"
    verbose_name = "Algorithms"
