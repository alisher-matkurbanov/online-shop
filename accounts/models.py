from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    auth_token = models.CharField(max_length=256)