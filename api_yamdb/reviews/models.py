from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_release_year(year):
    if year > timezone.now().year:
        raise ValidationError("Год выпуска не может быть больше текущего года.")
    

class Category(models.Model):
    """Модель Категории."""

    name = models.CharField(
        max_length=256,
        verbose_name='Категория')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    """Модель Жанры."""
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}'


class Titles(models.Model):
    """Модель Произведения."""
    name = models.CharField(max_length=200)
    year = models.IntegerField(validators=[validate_release_year])
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='titles')

    def __str__(self):
        return f'{self.name}'
