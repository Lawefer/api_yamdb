from django.db import models
#from api.v1.serializers import validate_release_year
from django.utils import timezone
from django.core.exceptions import ValidationError

class Category(models.Model):
    """Модель Категории."""

    name = models.CharField(
        max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    """Модель Жанры."""

    name = models.CharField(
        max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    """Модель Произведения."""

    def validate_release_year(year):
        if year and year > timezone.now().year:
            raise ValidationError("Год выпуска не может быть больше текущего года.")
        return year

    name = models.CharField(max_length=200)
    year = models.IntegerField(validators=[validate_release_year])
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='title')
    
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name}'
