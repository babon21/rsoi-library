from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AuthorSerializer, SaveBookSerializer, GetBookSerializer
from .models import Book, Author


@api_view(['GET', 'POST'])
def create_author_or_get_list(request):
    if request.method == 'GET':
        serializer = AuthorSerializer(Author.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        author = serializer.save()
        serializer = AuthorSerializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_book(request):
    serializer = SaveBookSerializer(data=request.data)
    if serializer.is_valid():
        book = serializer.save()
        serializer = SaveBookSerializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def get_or_delete_book(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GetBookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
