from rest_framework import viewsets, filters, status
from users.models import User
from api_yamdb.settings import EMAIL
from .serializers import UserSerializer, SignupSerializer, TokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from .permissions import IsOnlyAdmin, IsAdminOrReadOnly, IsOwnerOrModeratorOrAdmin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import uuid
from rest_framework_simplejwt.tokens import AccessToken


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username',)
    permission_classes = (IsOnlyAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=[IsAuthenticated, ]
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
    if username == 'me':
        return Response(
            'Такую учётную запись нельзя зарегестрировать',
            status=status.HTTP_400_BAD_REQUEST)
    user_email = User.objects.filter(email=email)
    user_name = User.objects.filter(username=username)
    if user_email.exists() or user_name.exists():
        return Response(
            status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = str(uuid.uuid4())
    User.objects.create(
        username=username,
        email=email,
        confirmation_code=confirmation_code)
    send_mail(
        subject='Код подтверждения yamdb.ru',
        message=f'"confirmation_code": "{confirmation_code}"',
        from_email=EMAIL,
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
