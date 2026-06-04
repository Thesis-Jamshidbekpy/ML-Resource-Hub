"""Serializers for account-facing API representations."""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    """Expose lightweight user identity fields."""

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class ProfileSerializer(serializers.ModelSerializer):
    """Serialize extended profile information for API reuse."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "user", "bio", "avatar", "institution", "academic_interest", "updated_at")
