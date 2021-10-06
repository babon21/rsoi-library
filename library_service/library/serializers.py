from abc import ABC

from rest_framework import serializers
from .models import Library, LibraryBook


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'city']


class LibraryBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBook
        fields = ['id', 'library', 'book_id', 'count']


class BooksSerializer(serializers.Serializer):
    books = serializers.ListField(
        child=serializers.IntegerField()
    )
