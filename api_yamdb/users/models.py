from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

ROLES = (('user', 'User'),
         ('moderator', 'Moder'),
         ('admin', 'Admin'),)


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=150,
                                unique=True,
                                blank=False,
                                null=False,
                                validators=[username_validator],
                                )
    email = models.EmailField(unique=True,
                              max_length=255,
                              blank=False,
                              null=False
                              )
    role = models.CharField(max_length=20,
                            choices=ROLES,
                            default='user',
                            blank=True
                            )
    confirmation_code = models.CharField(max_length=255,
                                         null=True,
                                         blank=False,
                                         )

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='О себе'
    )

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def __str__(self):
        return self.username
