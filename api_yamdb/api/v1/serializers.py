from rest_framework import serializers
from reviews.models import Title, Category, Genre, Review, Comment, Rating
from user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data.get('username') != 'me':
            return data
        raise serializers.ValidationError(
            'Некоректное имя пользователя.'
        )


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


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