from ast import mod
from django.db import models
from users.models import User


class BookManager(models.Manager):
        
        
    def create_book(self, author, title, author_book):
        book = self.model(author = User.objects.get(email = author), title=title, author_book=author_book)
        book.save()

        return book



class Books(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, primary_key=True)
    author_book = models.CharField(max_length=200)

    objects = BookManager()


class Category(models.Model):
    category = models.CharField(max_length=200)
    book = models.ManyToManyField(Books)


    def __str__(self):
        return self.category


