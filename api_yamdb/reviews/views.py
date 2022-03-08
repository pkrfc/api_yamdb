from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import mixins

from .permissions import IsOwnerOrReadOnly
from .models import Comment, Review
from .serializers import CommentSerializer, ReviewSerializer


class MyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                viewsets.GenericViewSet):

    pass


class ReviewViewSet(MyViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Review.objects.filter(user=self.request.user)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post_id)

    def get_queryset(self):
        post_id = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        queryset = post_id.comments.all()
        return queryset
