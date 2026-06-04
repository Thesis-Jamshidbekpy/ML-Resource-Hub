"""Signal handlers for keeping account-related data synchronized."""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """Ensure every authenticated user receives a profile record."""

    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile_for_existing_user(sender, instance, **kwargs):
    """Persist profile changes whenever the parent user is saved."""

    if hasattr(instance, "profile"):
        instance.profile.save()
