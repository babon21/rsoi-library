from django.urls import path
from .views import create_author_or_get_list, create_book_or_get_list, get_or_delete_book, search_by_book_name, \
    search_by_author

urlpatterns = [
    path('author', create_author_or_get_list),
    path('', create_book_or_get_list),
    path('<int:book_id>', get_or_delete_book),
    path('search_by_book_name/<str:book_name>', search_by_book_name),
    path('search_by_author/<str:author>', search_by_author),
]
