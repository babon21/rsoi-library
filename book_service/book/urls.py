from django.urls import path
from .views import create_author_or_get_list, create_book, get_or_delete_book

urlpatterns = [
    path('author', create_author_or_get_list),
    path('', create_book),
    path('<str:book_id>', get_or_delete_book),
]
