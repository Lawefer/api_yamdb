from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):

    """
    Разрешение только для администраторов,
    но для неизменяемых запросов разрешено всем.
    """

    def has_permission(self, request, view):
        # Разрешает GET, HEAD или OPTIONS запросы для всех пользователей
        if request.method in SAFE_METHODS:
            return True
        # Разрешает POST, PATCH или DELETE запросы только администраторам
        return request.user.is_superuser

class IsAuthorOrReadOnly(BasePermission):
    pass