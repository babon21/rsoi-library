from django.urls import path
from .views import create_library_or_get_libraries, add_or_remove_library_book, get_books, take_book, get_library, \
    return_book, get_taken_books

urlpatterns = [
    path('', create_library_or_get_libraries),
    path('<int:library_id>/book/<int:book_id>', add_or_remove_library_book),
    path('<int:library_id>/books', get_books),
    path('taked_books', get_taken_books),
    path('<int:library_id>', get_library),
    path('<int:library_id>/book/<int:book_id>/take', take_book),
    path('<int:library_id>/book/<int:book_id>/return', return_book),
]
