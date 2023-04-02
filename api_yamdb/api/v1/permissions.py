from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Дает полный доступ админу.

    Для остальных доступ только для безопасный запросов.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class AdminOnly(BasePermission):
    """Дает полный доступ админу."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsStafOrReadOnly(BasePermission):
    """Дает доступ авторизованному пользователю.

    Предоставляет возможность редактирования своих данных
    авторизованному пользователю. Так же админ и модератер
    имеют те же возможности. Для остальных доступ только
    для безопасный запросов.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            obj.author == request.user
            or (
                request.user.is_authenticated
                and (request.user.is_moder or request.user.is_admin)
            )
        )
