from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import routers

from .views import CategoriesViewSet, GenreViewSet, TitlesViewSet, UserViewSet, sign_up, token


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')



app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitlesViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', token, name='token'),

]
