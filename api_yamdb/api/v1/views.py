from rest_framework import generics
from rest_framework.generics import ListAPIView
from reviews.models import Category, Genre, Titles
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
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
#slug


class GenreViewSet(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ("name")


class TitleViewSet(generics.ListAPIView):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)

#дописать фильтрацию
