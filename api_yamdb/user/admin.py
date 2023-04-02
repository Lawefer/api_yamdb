from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка пользователей."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    empty_value_display = 'отсутствует'
    list_editable = ('role',)
    list_filter = ('username',)
    search_fields = ('username', 'role')
