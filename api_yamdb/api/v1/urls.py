from rest_framework import routers

from django.urls import include, path

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet,)


router_v1 = routers.DefaultRouter()

router_v1.register(r"titles", TitleViewSet, basename="title")
router_v1.register(r'genres', GenreViewSet, basename="genres")
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
    path('', include(router_v1.urls)),
]
