from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .permissions import (
    AdminOnlyOrReadOnly,
    IsAdminOrReadOnly,
    IsStafOrReadOnly,
)
from .serializers import (
    AccessTokenSerializer,
    CategorySerializer,
    CommentSerializer,
    CreateUserSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleListSerializer,
    UserSerializer,
)


class ListCreateDestroyViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    """Кастомный вьюсет.

    Предоставляет возможность просмотра, создания, удаления объектов.
    """

    pass


class UserViewSet(ModelViewSet):
    """Вьюсет пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "username"
    search_fields = ["username"]
    filter_backends = [SearchFilter]
    http_method_names = [
        "post",
        "patch",
        "get",
        "delete",
    ]

    @action(
        methods=[
            "get",
            "patch",
        ],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """Получение данных собственной учётной записи."""

        if request.method == "GET":
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            self.request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(
    [
        "POST",
    ]
)
@permission_classes([AllowAny])
def signup(request):
    """Регистрация пользователя."""

    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    email = serializer.validated_data.get("email")
    email_check = User.objects.filter(email=email).exists()
    username_check = User.objects.filter(username=username).exists()
    user_exists = email_check or username_check
    if user_exists:
        if email_check and not username_check:
            return Response(
                {"message": "Пользователь с таким email уже существует."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif not email_check and username_check:
            return Response(
                {"message": "Пользователь с таким username уже существует."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"message": "Пользователь уже зарегистрирован."},
                status=status.HTTP_200_OK,
            )
    user, code_created = User.objects.get_or_create(
        email=email,
        username=username,
    )
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        "Confirmation code",
        f"Ваш код подтверждения {confirmation_code}",
        None,
        [email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_jwt_token(request):
    """Токен."""
    serializer = AccessTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    confirmation_code = serializer.validated_data.get("confirmation_code")
    try:
        user = User.objects.get(
            username=username,
            confirmation_code=confirmation_code,
        )
    except User.DoesNotExist:
        return Response(
            {"message": "Токен не прошёл проверку"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user.confirmation_code = ""
    user.save()
    try:
        jwt_token = RefreshToken.for_user(user)
    except TokenError as e:
        return Response(
            {"message": f"Ошибка при создании токена: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(
        {"token": f"{jwt_token.access_token}"}, status=status.HTTP_200_OK
    )


class CategoryViewSet(ListCreateDestroyViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOnlyOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOnlyOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("name",)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(ModelViewSet):
    """Вьюсет для произведений."""

    queryset = (
        Title.objects.select_related("category")
        .prefetch_related("genre")
        .annotate(rating=Avg("reviews__score"))
        .order_by("name")
    )
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (AdminOnlyOrReadOnly,)
    filterset_class = TitleFilter
    filterset_fields = ("category", "genre", "name", "year")

    def get_serializer_class(self):
        if self.request.method in (
            "POST",
            "PATCH",
            "PUT",
        ):
            return TitleCreateSerializer
        return TitleListSerializer


class ReviewViewSet(ModelViewSet):
    """Вьюсет для отзывов на произведения."""

    queryset = Review.objects.select_related("title", "author")
    serializer_class = ReviewSerializer
    permission_classes = (IsStafOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title_object = Title.objects.get(id=title_id)
        serializer.save(author=self.request.user, title=title_object)


class CommentViewSet(ModelViewSet):
    """Вьюсет для комментираев на отзывы."""

    queryset = Comment.objects.select_related("review", "author")
    serializer_class = CommentSerializer
    permission_classes = (IsStafOrReadOnly,)

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review_object = Review.objects.get(id=review_id)
        serializer.save(author=self.request.user, review=review_object)
