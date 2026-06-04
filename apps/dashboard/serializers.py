"""Serializers for aggregated dashboard metrics."""

from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    """Represent summary metrics for potential future API expansion."""

    total_algorithms = serializers.IntegerField()
    total_resources = serializers.IntegerField()
    total_users = serializers.IntegerField()
