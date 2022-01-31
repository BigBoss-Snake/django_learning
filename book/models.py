from django.db import models
from users.models import User


class Books(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author_book = models.CharField(max_length=200)
