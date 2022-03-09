import uuid
from django.db.models import Avg
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Categories, Comment, Genres, Review, Title
from users.models import User

from .filters import TitlesFilter
from .pagination import TitlesPagination
from .permissions import (AdminOrReadOnly, IsOnlyAdmin, ReviewPermission, IsOwnerOrModeratorOrAdmin)
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenreSerializer, ProfileSerializer, ReviewSerializer,
                          SignupSerializer, TitlesSerializer, TokenSerializer,
                          UserSerializer)


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsOnlyAdmin,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=[IsAuthenticated, ],
        serializer_class=ProfileSerializer
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(
                data=serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(
                data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user_email = User.objects.filter(email=email)
    user_name = User.objects.filter(username=username)
    if user_email.exists() or user_name.exists():
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = str(uuid.uuid4())
    User.objects.create(
        username=username,
        email=email,
        confirmation_code=confirmation_code)
    send_mail(
        subject='Код подтверждения yamdb.ru',
        message=f'"confirmation_code": "{confirmation_code}"',
        from_email='yamdb@yamdb.ru',
        recipient_list=[email, ],
        fail_silently=True
    )
    return Response(
        data={'email': email, 'username': username},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes((AllowAny,))
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if confirmation_code != user.confirmation_code:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response({'token': f'{token}'}, status=status.HTTP_200_OK)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(
        detail=False, url_path=r'(?P<slug>\w+)',
        methods=['delete']
    )
    def destroy_category(self, request, slug):
        category = Categories.objects.filter(slug=slug)
        serializer = self.get_serializer(category, many=True)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(
        detail=False, url_path=r'(?P<slug>\w+)',
        methods=['delete']
    )
    def destroy_genre(self, request, slug):
        genre = Genres.objects.filter(slug=slug)
        serializer = self.get_serializer(genre, many=True)
        genre.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = TitlesPagination
    filterset_class = TitlesFilter

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__score')
        )


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewPermission]
    # permission_classes = [IsOwnerOrModeratorOrAdmin]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (filters.SearchFilter,)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewPermission]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        queryset = review.comments.all()
        return queryset
