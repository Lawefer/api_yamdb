from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import (ListModelMixin,
                                   CreateModelMixin,
                                   DestroyModelMixin)
from rest_framework.generics import ListAPIView 
from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleListSerializer,
                          TitleCreateSerializer, ReviewSerializer, CommentSerializer)
from .permissions import (
    AdminOnly,
    IsStafOrReadOnly,
    IsAdminOrReadOnly
)


class ListCreateDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("name")
    lookup_field = 'slug'


class GenreViewSet(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ("name")


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filterset_fields = ['category__slug', 'genre__slug', 'name', 'year']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT',):
            return TitleCreateSerializer
        return TitleListSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.select_related('title').select_related('author')
    serializer_class = ReviewSerializer
    permission_classes = (IsStafOrReadOnly,)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('review').select_related('author')
    serializer_class = CommentSerializer
    permission_classes = (IsStafOrReadOnly,)