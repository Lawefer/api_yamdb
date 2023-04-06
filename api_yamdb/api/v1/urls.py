from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    get_jwt_token,
    signup,
)


router_v1 = DefaultRouter()

router_v1.register(r"users", UserViewSet, basename="users")
router_v1.register(r"titles", TitleViewSet, basename="title")
router_v1.register(r"genres", GenreViewSet, basename="genres")
router_v1.register(r"categories", CategoryViewSet, basename="categories")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews\/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("auth/token/", get_jwt_token, name="token"),
    path("auth/signup/", signup),
    path("", include(router_v1.urls)),
]
