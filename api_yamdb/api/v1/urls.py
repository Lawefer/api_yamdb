from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)

router_v1 = routers.DefaultRouter()

# router_v1.register(r'titles', TitleViewSet, basename="titles")
# router_v1.register(r'genres', GenreViewSet, basename="genres")
# router_v1.register(r'categories', CategoryViewSet, basename="categories")
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename="reviews")
router_v1.register(r'comments', CommentViewSet, basename="comments")


urlpatterns = [
    path('', include(router_v1.urls))]
