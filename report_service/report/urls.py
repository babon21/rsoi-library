from django.urls import path

from .views import update_stat, GenreListView, take_stat, expire_stat, user_stat, in_time_stat

urlpatterns = [
    path('user/take', take_stat),
    path('user/expire', expire_stat),
    path('user/in_time', in_time_stat),
    path('user_stat', user_stat),

    path('genre/<int:book_id>', update_stat),
    path('genre_stat', GenreListView.as_view()),
]
