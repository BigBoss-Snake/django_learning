from django.db import models
from users.models import User


class BookManager(models.Manager):
    def create_book(self, author, title, category, author_book):
        _author = User.objects.get(email=author)
        _category = Category.objects.get(category=category.get('category', None))  # noqa: E501
        book = self.model(author=_author, title=title, author_book=author_book)
        book.save()
        book.category.add(_category)
        return book


class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category


class Value(models.Model):
    title = models.CharField(max_length=15)

    def __str__(self):
        return self.title


class Books(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.ManyToManyField(Category)
    author_book = models.CharField(max_length=200)
    value = models.ForeignKey(Value, on_delete=models.PROTECT)
    price = models.FloatField()

    objects = BookManager()

    def __str__(self):
        return self.title
