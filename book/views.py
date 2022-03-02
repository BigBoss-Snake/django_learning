from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Books, Category
from .renderers import BooksJSONRenderer
from .serialazers import BookSerializer, SearchSerialazer


def search_book_categorys(category):
    dict_id_category = []
    for object in category:
        id_category = Category.objects.get(category=object['category']).id
        dict_id_category.append(id_category)
    books = Books.objects.all()
    for id in dict_id_category:
        books = books.filter(category__id=id)
    return books


class CreateBook(APIView):
    permission_classes = (AllowAny,)
    serializer_class = BookSerializer
    renderer_classes = (BooksJSONRenderer, )

    book_response = openapi.Response('Книга создана')

    @swagger_auto_schema(
        operation_description="Метод создания книги в БД. "
                              "Ожидает в запросе почту автора, "
                              "название книги, жанр/ы, ФИО аватора, цена и в какой валюте цена.",  # noqa: E501
        request_body=BookSerializer,
        responses={201: book_response}
    )
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

    auth_response = openapi.Response('Информация о книге передана')

    @swagger_auto_schema(operation_description="Метод получения информации книги по её id",  # noqa: E501
                         responses={200: auth_response})
    def get(self, request, book_id):
        book = Books.objects.get(id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteBook(APIView):

    auth_response = openapi.Response('Книга удалена')

    @swagger_auto_schema(operation_description="Метод удаления книги по её id",  # noqa: E501
                         responses={204: auth_response})
    def delete(self, request, book_id):
        book = Books.objects.get(id=book_id)
        book.delete()
        return Response(f'Your delete book {book.title}', status=status.HTTP_204_NO_CONTENTD)  # noqa: E501


class ListBook(APIView):

    permission_classes = (AllowAny,)
    serializer_class = BookSerializer
    renderer_classes = (BooksJSONRenderer, )

    auth_response = openapi.Response('Список получен')

    @swagger_auto_schema(operation_description="Метод получения списка всех книг",  # noqa: E501
                         responses={200: auth_response})
    def get(self, request):
        all_book = Books.objects.all()
        return Response(BookSerializer(all_book, many=True).data, status=status.HTTP_200_OK)  # noqa: E501


class UpdateBook(APIView):

    permission_classes = (AllowAny,)
    serializer_class = BookSerializer
    renderer_classes = (BooksJSONRenderer, )

    book_response = openapi.Response('Книга обновлена')

    @swagger_auto_schema(
        operation_description="Метод обновления информации о книге в БД.",  # noqa: E501
        request_body=BookSerializer(),
        responses={200: book_response}
    )
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

    book_response = openapi.Response('Результат поиска')

    @swagger_auto_schema(
        operation_description="Метод поиска книги в БД по названию книги и/или категории.",  # noqa: E501
        request_body=SearchSerialazer,
        responses={200: book_response})
    def post(self, request):
        parametrs = request.data.get('parametrs', None)
        _title = parametrs.get('title', None)
        _category = parametrs.get('category', None)

        if _title and _category:
            books = search_book_categorys(_category)
            books = Books.objects.filter(title__icontains=_title)
        elif _title:
            books = Books.objects.filter(title__icontains=_title)
        elif _category:
            books = search_book_categorys(_category)
        else:
            books = Books.objects.all()

        return Response(BookSerializer(books, many=True).data, status=status.HTTP_200_OK)  # noqa: E501
