from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Дает полный доступ только админу.

    Для остальных доступа нет.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class AdminOnlyOrReadOnly(BasePermission):
    """Дает полный доступ админу.

    Для остальных только доступ к безопасным запросам.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


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
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
