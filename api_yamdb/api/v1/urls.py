from django.urls import include, path
from rest_framework import routers
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)

router_v1 = routers.DefaultRouter()

router_v1.register(r'titles', TitleViewSet, basename="title")
# router_v1.register(r'genres', GenreViewSet, basename="genres")
router_v1.register(r'categories', CategoryViewSet, basename="categories")
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews\/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
# router_v1.register(r'auth/signup', UserViewSet, basename='signup')


urlpatterns = [
    path('', include(router_v1.urls)),
    # path('auth/token/', TokenObtainPairView.as_view()),
]
