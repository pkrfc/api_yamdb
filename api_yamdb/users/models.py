from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = models.CharField(max_length=150,
                                unique=True,
                                blank=False,
                                null=False
                                )
    email = models.EmailField(unique=True,
                              max_length=255,
                              blank=False,
                              null=False
                              )
    role = models.CharField()
    confirmation_code = models.CharField()
