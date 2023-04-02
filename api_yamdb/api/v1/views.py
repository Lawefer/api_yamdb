from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin,)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Review, Comment
from user.conf_mail import confirmation_generator
from user.models import User

from .permissions import AdminOnly, IsAdminOrReadOnly, IsStafOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          ObtainTokenSerializer, RegistrationSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          UserSerializer, ReviewSerializer, CommentSerializer)


class ListCreateDestroyViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    pass


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = request.data.get('username')
            confirmation_generator(username)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AuthTokenView(APIView):
    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            confirmation_code = serializer.data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if confirmation_code != user.confirmation_code:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    lookup_field = "username"

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.validated_data['role'] = request.user.role
                serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = "name"
    lookup_field = "slug"


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = "name"


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug', 'genre__slug', 'name', 'year']

    def get_serializer_class(self):
        if self.request.method in (
            "POST",
            "PATCH",
            "PUT",
        ):
            return TitleCreateSerializer
        return TitleListSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.select_related("title").select_related("author")
    serializer_class = ReviewSerializer
    permission_classes = (IsStafOrReadOnly,)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related("review").select_related(
        "author"
    )
    serializer_class = CommentSerializer
    permission_classes = (IsStafOrReadOnly,)
