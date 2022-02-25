from rest_framework.response import Response
from .models import Books, Category
from .renderers import BooksJSONRenderer
from rest_framework.views import APIView
from .serialazers import BookSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status


def create_list_category(category):
    dict_id_category = []
    for object in category:
        id_category = Category.objects.get(category=object['category']).id
        dict_id_category.append(id_category)
    return dict_id_category


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
        return Response(BookSerializer(all_book, many=True).data, status=status.HTTP_200_OK)  # noqa: E501


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
        _title = parametrs.get('title', None)
        _category = parametrs.get('category', None)

        if _title and _category:
            books = Books.objects.filter(title__icontains=_title).filter(category__id=create_list_category(_category))  # noqa: E501
        elif _title:
            books = Books.objects.filter(title__icontains=_title)
        else:
            id_categorys = create_list_category(_category)
            print(id_categorys)
            books = Books.objects.all()  # noqa: E501
            for id in id_categorys:
                books = books.filter(category__id=id)  # noqa: E501
        return Response(BookSerializer(books, many=True).data, status=status.HTTP_200_OK)  # noqa: E501
