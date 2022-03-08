from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import UserViewSet, sign_up, token

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

from rest_framework import routers

from api.views import CategoriesViewSet, GenreViewSet, TitlesViewSet

app_name = 'api'


router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitlesViewSet)
>>>>>>> origin/develop_2


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', token, name='token'),

]
