from rest_framework import serializers
from users.models import User

class BookSerializer(serializers.Serializer):
    author = serializers.ForeignKey(User)
    title = serializers.CharField(max_length=200)
    author_book = serializers.CharField(max_length=200)
    
