from django.urls import path

from .views import *

urlpatterns = [
    path('', get_rating),
    path('/', get_rating),
    path('up', up),
    path('down', down),
]
