from rest_framework import serializers

from django.utils import timezone

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleListSerializer(serializers.ModelSerializer):
    """Показ произведений"""

    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        queryset=Genre.objects.all(),
    )
    name = serializers.CharField(required=False)
    year = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = ("id", "name", "year", "category", "genre")


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all(), required=True
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        queryset=Genre.objects.all(),
        required=True,
    )
    name = serializers.CharField(max_length=256, required=True)
    year = serializers.IntegerField(required=True)

    class Meta:
        model = Title
        fields = ("id", "name", "year", "category", "genre", "description")

    def validate_year(self, year):
        if year and year > timezone.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего."
            )
        return year


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("author", "pub_date")


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")
        read_only_fields = ("author", "pub_date")
