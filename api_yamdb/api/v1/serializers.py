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

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    name = serializers.CharField(required=False)
    year = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")


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
        fields = ("id", "name", "year", "description", "genre", "category")

    def validate_year(self, year):
        if year and year > timezone.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего."
            )
        return year


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")
        read_only_fields = ("author", "pub_date")

    def validate(self, data):
        request = self.context['request']
        title_id = self.context.get('view').kwargs.get('title_id')
        author_id = self.context.get("request").user.id

        if (
            request.method == "POST"
            and Review.objects.filter(title_id=title_id, author_id=author_id
                                      ).exists()):
            raise serializers.ValidationError(
                "Review to this title already exist"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", 'pub_date')
        read_only_fields = ("author", "pub_date")
