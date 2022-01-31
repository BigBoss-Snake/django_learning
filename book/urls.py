from django.urls import path
from . import views


urlpatterns = [
    path('', views.BookListView.as_view(), name='books'),
    path('list/', views.index, name='index'),
    path('<int:book_id>/', views.detail, name='detail'),
    path('update/', views.update, name='index'),
    path('update/create/', views.create),
    path('delete/<int:book_id>/', views.delete, name='delete'),
]