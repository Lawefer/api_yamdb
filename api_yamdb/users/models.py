from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models


class RoleChoices(Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"

    @classmethod
    def choices(cls):
        return tuple((role.name, role.value) for role in cls)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        unique=True,
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name="Роль",
        max_length=100,
        choices=RoleChoices.choices(),
        default=RoleChoices.user.name,
    )
    confirmation_code = models.CharField(
        verbose_name="Код подтверждения",
        max_length=150,
        editable=False,
        null=True,
        blank=True,
        unique=False,
    )

    @property
    def is_user(self):
        """Проверяем наличие прав пользователя."""
        return self.role == RoleChoices.user.name

    @property
    def is_admin(self):
        """Проверяемм наличие прав администратора."""
        return any(
            [
                self.role == RoleChoices.admin.name,
                self.is_superuser,
                self.is_staff,
            ]
        )

    @property
    def is_moderator(self):
        """Проверяем наличие прав модератора."""
        return self.role == RoleChoices.moderator.name

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"
        ordering = ("username",)
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_username_email"
            )
        ]

    def __str__(self):
        return self.username
