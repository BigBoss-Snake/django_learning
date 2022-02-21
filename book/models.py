from django.db import models
from users.models import User


class BookManager(models.Manager):
    def create_book(self, author, title, category, author_book, value, price):
        _author = User.objects.get(email=author)
        # _category = category.get('category', None)  # noqa: E501
        _value = Value.objects.get(title=value)
        _price = price
        print(_price)
        book = self.model(author=_author, title=title, author_book=author_book, value=_value, price=price)  # noqa: E501
        book.save()
        book.category.add(category)
        return book


class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category


class Value(models.Model):
    title = models.CharField(max_length=15)
    count = models.FloatField()

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
