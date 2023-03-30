from rest_framework import generics
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from reviews.models import Category, Genre, Title, Review, Comment, Rating
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, ReviewSerializer, CommentSerializer, RatingSerializer, RatingSerializer
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .permissions import (
    AdminOnly,
    IsStafOrReadOnly,
    IsAdminOrReadOnly
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CategoryViewSet(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("name")


class GenreViewSet(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ("name")


class TitleViewSet(generics.ListAPIView):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    ###дописать фильтрацию 


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('title').select_related('author')
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('review').select_related('author')
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)