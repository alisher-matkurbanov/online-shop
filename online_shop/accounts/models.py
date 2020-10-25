from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

USERNAME_LENGTH = 15
PASSWORD_LENGTH = 128


class Account(AbstractUser):
    username = models.CharField(max_length=USERNAME_LENGTH, unique=True)
    password = models.CharField(max_length=PASSWORD_LENGTH)
