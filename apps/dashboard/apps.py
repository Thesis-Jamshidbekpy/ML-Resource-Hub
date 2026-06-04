"""Application configuration for dashboard and landing pages."""

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """Declare metadata for the dashboard app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"
    label = "dashboard"
    verbose_name = "Dashboard"
