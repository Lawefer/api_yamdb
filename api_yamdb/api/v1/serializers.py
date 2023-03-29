from rest_framework import serializers
from reviews.models import Titles, Category, Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Titles
        fields = ['name', 'year', 'description', 'genre', 'category']       