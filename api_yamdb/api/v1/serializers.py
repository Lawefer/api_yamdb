from rest_framework import serializers
from reviews.models import Title, Category, Genre, Review, Comment, Rating


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
    # добавить средний рейтинг (скрин в дискорде)

    class Meta:
        model = Title
        fields = ['name', 'year', 'description', 'genre', 'category']      

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('review', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'pub_date')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'pub_date') 