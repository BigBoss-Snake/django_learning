from django.urls import path
from . import views
from .views import RegistrationAPIView, LoginAPIView


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', RegistrationAPIView.as_view(), name='create'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate')
    ]
