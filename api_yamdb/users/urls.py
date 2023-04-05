from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import UserViewSet, get_jwt_token, signup


app_name = "users"

users_router = DefaultRouter()
users_router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("auth/token/", get_jwt_token, name="token"),
    path("auth/signup/", signup),
    path("", include(users_router.urls)),
]
