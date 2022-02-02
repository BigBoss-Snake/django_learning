from django.shortcuts import render
from httplib2 import Response
from .models import Books
from .renderers import BooksJSONRenderer
from django.http import JsonResponse, HttpResponseRedirect
from django.views import generic
from rest_framework.views import APIView
from .serialazers import BookSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status


class CreateBook(APIView):
    permission_classes = (AllowAny,)
    serializer_class = BookSerializer
    render_class = (BooksJSONRenderer, )

    def post(self, request):
        book = request.data.get('book', {})
        serializer = self.serializer_class(data=book)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)



class DetaelBook(APIView):

    permission_classes = (AllowAny,)
    serializer_class = BookSerializer
    render_class = (BooksJSONRenderer, )

    def get(self, request, book_id):
        book = Books.objects.get(id = book_id)
        serialazer = BookSerializer(book)
        return Response(serialazer.data, status = status.HTTP_200_OK)

