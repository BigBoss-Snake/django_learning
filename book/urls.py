from django.urls import path
from . import views
from .views import CreateBook, DeleteBook, DetaelBook


urlpatterns = [
    # path('', views.BookListView.as_view(), name='books'),
    path('create/', CreateBook.as_view(), name = 'create'),
    # path('list/', views.index, name='index'),
    path('<int:book_id>/', DetaelBook.as_view(), name='detail'),
    # path('update/', views.update, name='index'),
    # path('update/create/', views.create),
    path('delete/<int:book_id>/', DeleteBook.as_view(), name='delete'),
]