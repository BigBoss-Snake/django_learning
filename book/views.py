from django.shortcuts import render
from .models import Books
from django.http import JsonResponse, HttpResponseRedirect
from django.views import generic
from rest_framework.views import APIView
from .serialazers import BookSerializer
from rest_framework.permissions import AllowAny


class CreateBook(APIView):
    permission_classes = (AllowAny,)
    serializer_class = BookSerializer

    def post(self, request):
        book = request.data.get('book', {})
        serializer = self.serializer_class(data=book)
        serializer.is_valid(raise_exception=True)
        serializer.save()


def book_to_dict(book):
    output = {}
    output['title'] = book.title
    output['author_book'] = book.author_book

    return output


def index(request):
    all_obj = Books.objects.all()

    dict_book = []

    for i in range(len(all_obj)):
        dict_book.append(book_to_dict(all_obj[i]))

    return JsonResponse(dict_book, content_type="book.html", safe=False)


def detail(request, book_id):
    search_book = []
    search_book = Books.objects.get(id = book_id)
    data = book_to_dict(search_book)
    return JsonResponse(data)

def update(request):
    return render (request, 'update.html')

def create(request):
        # if request.method == "POST":
        #     new_book = Books()
        #     author_id = Authors.objects.get(last_name = request.POST.get("author"))
        #     new_book.author = author_id
        #     new_book.title = request.POST.get("title")
        #     new_book.author_book = request.POST.get("author_book")
        #     new_book.save()  
        return HttpResponseRedirect('/')

def delete(request, book_id):
    book = Books.objects.get(id = book_id)
    book.delete()
    return HttpResponseRedirect('/')
