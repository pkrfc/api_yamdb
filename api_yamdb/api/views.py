
from rest_framework import filters, mixins, viewsets
from api.pagination import ReviewsPagination
from django_filters.rest_framework import DjangoFilterBackend

from api.permissions import AdminOrReadOnly
from reviews.models import Categories, Genres, Titles

from .serializers import (
    CategoriesSerializer,
    GenreSerializer,
    TitlesSerializer
)


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class CategoriesViewSet(CreateListViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = ReviewsPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = ReviewsPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = ReviewsPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'category', 'genre', 'name', 'year'
    )
