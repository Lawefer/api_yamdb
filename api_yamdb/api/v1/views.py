from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin,)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from reviews.models import Category, Comment, Genre, Review, Title

from .permissions import IsAdminOrReadOnly, IsStafOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleListSerializer
)


class ListCreateDestroyViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    pass


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

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title_object = Title.objects.get(id=title_id)
        serializer.save(author=self.request.user, title=title_object)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related("review").select_related(
        "author"
    )
    serializer_class = CommentSerializer
    permission_classes = (IsStafOrReadOnly,)

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review_object = Review.objects.get(id=review_id)
        serializer.save(author=self.request.user, review=review_object)
