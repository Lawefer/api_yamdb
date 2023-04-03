from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from user.models import User


def validate_release_year(year):
    if year and year > timezone.now().year:
        raise ValidationError(
            "Год выпуска не может быть больше текущего года."
        )
    return year


class Category(models.Model):
    """Модель Категории."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"


class Genre(models.Model):
    """Модель Жанры."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return f"{self.name}"


class Title(models.Model):
    """Модель Произведения."""

    name = models.CharField(max_length=200)
    year = models.IntegerField(validators=[validate_release_year])
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre, related_name="titles", blank=True,
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="title"
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return f"{self.name}"


class GenreTitle(models.Model):
    """Вспомогательный класс, связывающий жанры и произведения."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )

    class Meta:
        verbose_name = 'Соответствие жанра и произведения'
        verbose_name_plural = 'Таблица соответствия жанров и произведений'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} принадлежит жанру/ам {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    score = models.IntegerField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Отзывы"
        verbose_name = "Отзыв"
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_author_title"
            ),
        ]

    def __str__(self):
        return self.text

class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Комментарии"
        verbose_name = "Комментарий"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
