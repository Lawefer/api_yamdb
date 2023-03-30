from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Класс пользователей."""

    class Roles(models.TextChoices):
        user = 'user', 'Пользователь'
        moderator = 'moderator', 'Модератор'
        admin = 'admin', 'Админ'

    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ.'
        )]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=20,
        verbose_name='Роль',
        choices=Roles.choices,
        default=Roles.user,
    )
    confirmation_code = models.CharField(
        'Код авторизации',
        max_length=20,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_username_email"
            ),
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.is_superuser or self.role == self.Roles.admin or self.is_staff
        )

    @property
    def is_moder(self):
        return self.role == self.Roles.moderator
