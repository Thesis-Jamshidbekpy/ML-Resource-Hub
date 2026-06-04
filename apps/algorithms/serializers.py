"""Serializers for algorithms, comments, ratings, and category metadata."""

from rest_framework import serializers

from .models import Algorithm, AlgorithmCategory, Comment, Rating


class AlgorithmSerializer(serializers.ModelSerializer):
    """Serialize algorithm records for list and detail API endpoints."""

    category_display = serializers.CharField(source="get_category_display", read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    ratings_count = serializers.IntegerField(read_only=True)
    localized_name = serializers.CharField(read_only=True)
    localized_algorithm_type = serializers.CharField(read_only=True)
    localized_description = serializers.CharField(read_only=True)

    class Meta:
        model = Algorithm
        fields = (
            "id",
            "name",
            "name_uz",
            "localized_name",
            "slug",
            "category",
            "category_display",
            "algorithm_type",
            "algorithm_type_uz",
            "localized_algorithm_type",
            "description",
            "description_uz",
            "localized_description",
            "mathematical_foundation",
            "mathematical_foundation_uz",
            "advantages",
            "advantages_uz",
            "disadvantages",
            "disadvantages_uz",
            "applications",
            "applications_uz",
            "complexity",
            "complexity_uz",
            "image",
            "view_count",
            "average_rating",
            "ratings_count",
            "created_at",
            "updated_at",
        )


class CategorySerializer(serializers.Serializer):
    """Expose algorithm category choices as API-friendly label/value pairs."""

    value = serializers.CharField()
    label = serializers.CharField()

    @staticmethod
    def from_choices():
        return [{"value": value, "label": label} for value, label in AlgorithmCategory.choices]


class CommentSerializer(serializers.ModelSerializer):
    """Serialize user comments with denormalized author context."""

    user_username = serializers.CharField(source="user.username", read_only=True)
    algorithm_name = serializers.CharField(source="algorithm.name", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "user", "user_username", "algorithm", "algorithm_name", "text", "created_at")
        read_only_fields = ("user", "created_at")


class RatingSerializer(serializers.ModelSerializer):
    """Serialize numeric evaluations for authenticated API users."""

    user_username = serializers.CharField(source="user.username", read_only=True)
    algorithm_name = serializers.CharField(source="algorithm.name", read_only=True)

    class Meta:
        model = Rating
        fields = (
            "id",
            "user",
            "user_username",
            "algorithm",
            "algorithm_name",
            "score",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("user", "created_at", "updated_at")
