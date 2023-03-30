from rest_framework import serializers
from reviews.models import Title, Category, Genre
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleListSerializer(serializers.ModelSerializer):
    """Показ произведений"""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
 
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),

    )
    name = serializers.CharField(required=False)
    year = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'genre')


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        required=True
    )
    name = serializers.CharField(max_length=256, required=True)
    year = serializers.IntegerField(required=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'genre', 'description')

    def validate_year(self, year):
        if year and year > timezone.now().year:
            raise serializers.ValidationError("Год выпуска не может быть больше текущего.")
        return year







#class TitleSerializer(serializers.ModelSerializer):
 #   genre = GenreSerializer(many=True)
  #  category = serializers.CharField(source='category.name')
#
  #  class Meta:
 #       model = Title
 #       fields = ['name', 'year', 'description', 'genre', 'category']
#
#    def validate_year(self, year):
#        if year > timezone.now().year:
#            raise ValidationError("Год выпуска не может быть больше текущего года.")
#        return year