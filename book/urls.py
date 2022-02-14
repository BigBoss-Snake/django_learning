from django.urls import path
from . import views
from .views import (
    CreateBook, DeleteBook, DetaelBook, ListBook, SearchBook, UpdateBook
)


urlpatterns = [

    path('create/', CreateBook.as_view(), name='create'),
    path('list/', ListBook.as_view(), name='list'),
    path('<int:book_id>/', DetaelBook.as_view(), name='detail'),
    path('update/', UpdateBook.as_view(), name='update'),
    path('delete/<int:book_id>/', DeleteBook.as_view(), name='delete'),
    path('search/', SearchBook.as_view(), name='search')
    ]
