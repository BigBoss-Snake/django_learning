import email
from pyexpat import model
from rest_framework import serializers
from book.models import Books
from users.models import User

class BookSerializer(serializers.Serializer):
    author = serializers.CharField(max_length=200)
    title = serializers.CharField(max_length=200)
    author_book = serializers.CharField(max_length=200)

    class Meta:
        model = Books
        fields = ('author', 'title', 'author_book')

    def create(self, validated_data):
        return Books.objects.create_book(**validated_data)

    def validate(self, data):
        author = data.get('author', None)
        title = data.get('title', None)
        author_book = data.get('author_book', None)     
        lol = User.objects.filter(email=author)

        if author is None:
            raise serializers.ValidationError(
                'The name author is not enered'
            )

        if title is None:
            raise serializers.ValidationError(
                'The name of the book is not entered'
            )

        if author_book is None:
            raise serializers.ValidationError(
                'The author of the book is not entered    '
            )

        if not User.objects.filter(email=author):
            raise serializers.ValidationError(
                'This author does not exist'
            )
        

        return {
                'author': author,
                'title': title,
                'author_book': author_book
            }
    
