from rest_framework import serializers

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для класса пользователь"""

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
    """Сериалайзер для регистрации пользователей"""

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
        """Проверка имя пользователя"""

        if data["username"] == "me":
            raise serializers.ValidationError(
                {"Выберете другое имя пользователя"}
            )
        return data


class AccessTokenSerializer(serializers.Serializer):
    """Сериалайзер для получения JWT-токена"""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        """Проверка кода подтверждения"""

        user = get_object_or_404(User, username=data["username"])
        if not default_token_generator.check_token(
            user, data["confirmation_code"]
        ):
            raise serializers.ValidationError(
                {"confirmation_code": "Ошибка при вводе кода подтверждения"}
            )
        return data
