from rest_framework import serializers

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils import timezone

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для класса пользователь."""

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "bio",
            "email",
            "role",
        ]


class CreateUserSerializer(serializers.Serializer):
    """Сериалайзер для регистрации пользователей."""

    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.RegexField(
        required=True,
        max_length=150,
        regex=r"^[\w.@+-]+\Z",
    )

    def validate(self, data):
        """Проверка имя пользователя."""
        if data["username"] == "me":
            raise serializers.ValidationError(
                {"Выберете другое имя пользователя"}
            )
        return data


class AccessTokenSerializer(serializers.Serializer):
    """Сериалайзер для получения JWT-токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        """Проверка кода подтверждения."""
        user = get_object_or_404(User, username=data["username"])
        if not default_token_generator.check_token(
            user, data["confirmation_code"]
        ):
            raise serializers.ValidationError(
                {"confirmation_code": "Ошибка при вводе кода подтверждения"}
            )
        return data


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатор произведений при SAFE запросе."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    name = serializers.CharField(required=False)
    year = serializers.IntegerField(required=False)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор произведений при не SAFE запросе."""

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
    year = serializers.IntegerField()

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
    """Сериализатор отзывов на произведения."""

    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")
        read_only_fields = ("author", "pub_date")

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("Score must be between 0 and 10")
        return value

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context.get("view").kwargs.get("title_id")
        author_id = self.context.get("request").user.id

        if (
            request.method == "POST"
            and Review.objects.filter(
                title_id=title_id, author_id=author_id
            ).exists()
        ):
            raise serializers.ValidationError(
                "Review to this title already exist"
            )
        get_object_or_404(Title, id=title_id)
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев на отзывы."""

    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("author", "pub_date")

    def validate(self, data):
        title_id = self.context.get("view").kwargs.get("review_id")
        get_object_or_404(Review, id=title_id)
        return data
