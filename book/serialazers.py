import email
from pyexpat import model
from rest_framework import serializers
from book.models import Books
from users.models import User

class BookSerializer(serializers.Serializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.get(email))
    title = serializers.CharField(max_length=200)
    author_book = serializers.CharField(max_length=200)

    class Meta:
        model = Books
        fields = ('author', 'title', 'author_book')

    def create(self, validated_data):
        a = User(validated_data)
        a.save()
        return a

    # def validate(self, data):
    #     title = data.get('title', None)
    #     author_book = data.get('author_book', None)
        

    #     if title is None:
    #         raise serializers.ValidationError(
    #             'The name of the book is not entered'
    #         )

    #     if author_book is None:
    #         raise serializers.ValidationError(
    #             'The author of the book is not entered    '
    #         )
        

    #     return {
    #             # 'author': email,
    #             'title': title,
    #             'author_book': author_book
    #         }
    
