from django.urls import path
from .views import register, login, validate, logout

urlpatterns = [
    path('signup', register),
    path('login', login),
    path('logout', logout),
    path('validate', validate),
    # path('', create_book),
]
