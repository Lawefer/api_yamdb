from rest_framework import routers

from django.urls import include, path

from .views import (AuthTokenView, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet,
                    UserRegistrationView, UserViewSet,)


router_v1 = routers.DefaultRouter()

router_v1.register(r'title', TitleViewSet, basename="title")
router_v1.register(r'genres', GenreViewSet, basename="genres")
router_v1.register(r'categories', CategoryViewSet, basename="categories")
router_v1.register(
    r'title\/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'title\/(?P<title_id>\d+)/reviews\/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register('users', UserViewSet, basename="user")


urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/signup/', UserRegistrationView.as_view(), name="signup"),
    path('v1/auth/token/', AuthTokenView.as_view(), name="auth"),
]
