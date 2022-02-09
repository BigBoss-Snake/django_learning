from rest_framework.response import Response
from .models import Books
from .renderers import BooksJSONRenderer
from rest_framework.views import APIView
from .serialazers import BookSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status


class CreateBook(APIView):
    permission_classes = (AllowAny,)
    serializer_class = BookSerializer
    renderer_classes = (BooksJSONRenderer, )

    def post(self, request):
        book = request.data.get('book', {})
        serializer = self.serializer_class(data=book)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DetaelBook(APIView):

    permission_classes = (AllowAny,)
    serializer_class = BookSerializer
    renderer_classes = (BooksJSONRenderer, )

    def get(self, request, book_id):
        book = Books.objects.get(id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteBook(APIView):

    def delete(self, request, book_id):
        book = Books.objects.get(id=book_id)
        book.delete()
        return Response(f'Your delete book {book.title}', status=status.HTTP_204_NO_CONTENTD)  # noqa: E501


class ListBook(APIView):

    permission_classes = (AllowAny,)
    serializer_class = BookSerializer

    def get(self, request):
        all_book = Books.objects.all()

        dict_book = []

        for i in range(len(all_book)):
            dict_book.append({'book': BookSerializer(all_book[i]).data})

        return Response(dict_book, status=status.HTTP_200_OK)


class UpdateBook(APIView):

    permission_classes = (AllowAny,)
    serializer_class = BookSerializer
    renderer_classes = (BooksJSONRenderer, )

    def put(self, request):
        book = request.data.get('book', {})
        serializer = self.serializer_class(data=book)
        serializer.is_valid(raise_exception=True)
        update_book = Books.objects.get(title=serializer.data.get('title'))
        update_book.author_book = serializer.data.get('author_book')
        update_book.save()
        serializers = BookSerializer(update_book)

        return Response(serializers.data, status=status.HTTP_200_OK)


class SearchBook(APIView):

    permission_classes = (AllowAny,)
    serializer_class = BookSerializer
    renderer_classes = (BooksJSONRenderer, )

    def get(self, request):
        parametrs = request.data.get('parametrs', None)
        books = Books.objects.filter(title=parametrs.get('parametrs', None))
        
        return
        
