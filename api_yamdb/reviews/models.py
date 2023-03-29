from django.db import models
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError
from django.utils import timezone

User = get_user_model()

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

class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        ordering = ['-pub_date']
    
    def __str__(self):
        return self.text

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['-pub_date']
    
    def __str__(self):
        return self.text
    
class Rating(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    grade = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Рейтинги'
        verbose_name = 'Рейтинг'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "title"], name="unique_user_title"
            ),
        ]
