"""Application configuration for account management."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configure account-related startup hooks."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    label = "accounts"
    verbose_name = "Accounts"

    def ready(self) -> None:
        """Import signals once the Django app registry is ready."""

        from . import signals  # noqa: F401
