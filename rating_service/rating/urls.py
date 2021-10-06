from django.urls import path

from .views import *

urlpatterns = [
    path('up', up),
    path('down', down),
    path('', get_rating),
]
