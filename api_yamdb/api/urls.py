from django.urls import include, path
from rest_framework import routers

from api.views import CategoriesViewSet, GenreViewSet, TitlesViewSet

app_name = 'api'


router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitlesViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
