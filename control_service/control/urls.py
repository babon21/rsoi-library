from django.urls import path
from .views import take_book, return_book, up, get_monitoring

urlpatterns = [
    path('take', take_book),
    path('return', return_book),
    path('up', up),
    path('get', get_monitoring),
]
