from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import (ListModelMixin,
                                   CreateModelMixin,
                                   DestroyModelMixin)
from rest_framework.generics import ListAPIView
from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleListSerializer,
                          TitleCreateSerializer)
from .permissions import (
    AdminOnly,
    IsStafOrReadOnly,
    IsAdminOrReadOnly
)


class ListCreateDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               ):
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


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('title').select_related('author')
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('review').select_related('author')
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)