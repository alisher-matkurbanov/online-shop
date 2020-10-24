from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField()


class Review(models.Model):
    rate = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    comment = models.TextField()
    user = models.ForeignKey('accounts.User', related_name='reviews', on_delete=models.CASCADE)
