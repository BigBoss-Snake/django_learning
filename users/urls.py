from django.urls import path
from . import views
from .views import RegistrationAPIView


urlpatterns = [
    path('', views.index, name = 'index'),
    path('create/', RegistrationAPIView.as_view(), name = 'index'), 
]