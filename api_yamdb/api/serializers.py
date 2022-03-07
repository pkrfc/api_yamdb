from rest_framework import serializers
from users.models import User, ROLES
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLES, default='user')

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')
        model = User


class ProfileSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Регистрация с username me запрещена')
        return value

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )
