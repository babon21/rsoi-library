from django.urls import path
from .views import signup, make_login, index, library_books, admin, add_library_admin, add_book_admin, \
    add_library_book, make_logout, take_book, user_books, return_book, genre_stat, user_stat, delete_library_book, \
    delete_book, user_rating, search_by_book_name, search_by_author, search

urlpatterns = [
    # VIEW
    # path('books/', books),
    path('index/', index, name="index"),
    path('login', make_login, name="login"),
    path('logout', make_logout, name="logout"),
    path('signup', signup, name="signup"),
    path('library/<int:library_id>/books', library_books, name="books"),
    path('admin', admin, name="admin"),
    path('take_book/<int:library_id>/<int:book_id>', take_book, name="take_book"),
    path('user_books/', user_books, name="user_books"),
    path('return_book/<int:book_id>', return_book, name="return_book"),

    path('rating/', user_rating, name="rating"),
    path('search/', search, name="search"),
    path('search_by_book_name/', search_by_book_name, name="search_by_book_name"),
    path('search_by_author/', search_by_author, name="search_by_author"),

    # admin operation
    path('add_library', add_library_admin, name="add_library"),
    path('add_book', add_book_admin, name="add_book"),
    path('add_library_book', add_library_book, name="add_book_to_library"),
    path('delete_library_book/<int:library_id>/<int:book_id>', delete_library_book, name="delete_library_book"),
    path('delete_book', delete_book, name="delete_book"),
    path('genre_stat/', genre_stat, name="genre_stat"),
    path('user_stat/', user_stat, name="user_stat"),
]
