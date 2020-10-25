from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

USERNAME_LENGTH = 15
PASSWORD_LENGTH = 128

class User(AbstractUser):
    username = models.CharField(max_length=USERNAME_LENGTH, unique=True)
    password = models.CharField(max_length=PASSWORD_LENGTH)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
