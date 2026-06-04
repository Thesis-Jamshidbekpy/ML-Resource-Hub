"""Application configuration for learning resources."""

from django.apps import AppConfig


class ResourcesConfig(AppConfig):
    """Declare metadata for the resources app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.resources"
    label = "resources"
    verbose_name = "Resources"
