import datetime
import json

import jwt
import pytz
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import LibraryBook, Library, TakenBook
from .serializers import LibrarySerializer, LibraryBookSerializer
from library_service.settings import JWT_KEY

BOOK_URL = "localhost:9002"
SESSION_URL = "127.0.0.1:9003/api/v1/session"
REPORT_URL = "127.0.0.1:9004/api/v1/report"
RATING_URL = "127.0.0.1:9005/api/v1/rating"
CONTROL_URL = "127.0.0.1:9006/api/v1/control"
tz_MOS = pytz.timezone('Europe/Moscow')


def cookies(request):
    is_authenticated = False
    session = requests.get(f"http://{SESSION_URL}/validate", cookies=request.COOKIES)
    if session.status_code != 200:
        pass
        # if session.status_code == 403:
        #     session = requests.get("http://localhost:8001/api/v1/session/refresh", cookies=request.COOKIES)
        #     is_authenticated = True
        # elif session.status_code == 401:
        #     pass
        # else:
        #     request.delete_cookie('jwt')
    else:
        is_authenticated = True
    return is_authenticated, request, session


def auth(request):
    token = request.COOKIES.get('jwt')

    if not token:
        return
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=['HS256'], options={"verify_exp": False})
    except jwt.DecodeError:
        return None
    return payload


@api_view(['GET', 'POST'])
def create_library_or_get_libraries(request):
    if request.method == 'GET':
        serializer = LibrarySerializer(Library.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = LibrarySerializer(data=request.data)
    if serializer.is_valid():
        library = serializer.save()
        serializer = LibrarySerializer(library)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'DELETE'])
def add_or_remove_library_book(request, library_id, book_id):
    try:
        library_book = LibraryBook.objects.get(library_id=library_id, book_id=book_id)
        if request.method == 'DELETE':
            if library_book.count > 0:
                library_book.count -= 1
                library_book.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        library_book.count += 1
    except LibraryBook.DoesNotExist:
        if request.method == 'DELETE':
            return Response(status=status.HTTP_404_NOT_FOUND)

        library_book = LibraryBook()
        library = Library()
        library.id = library_id
        library_book.library = library
        library_book.book_id = book_id
        library_book.count = 1

    library_book.save()
    serializer = LibraryBookSerializer(library_book)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_books(request, library_id):
    data = auth(request)
    if data['role'] != 'admin':
        taken_book = list(TakenBook.objects.filter(user_id=data['user_id']).values_list('book_id', flat=True))

        books = list(LibraryBook.objects.filter(library_id=library_id).exclude(book_id__in=taken_book).values('book_id', 'count'))

    else:
        books = list(LibraryBook.objects.filter(library_id=library_id).values('book_id', 'count'))

    book_infos = []
    for book in books:
        service_response = requests.get(f"http://{BOOK_URL}/api/v1/book/{book['book_id']}")
        if service_response.status_code == status.HTTP_404_NOT_FOUND:
            continue
        book_info = service_response.json()
        book_info['count'] = book['count']
        book_infos.append(book_info)

    return Response(book_infos)


@api_view(['POST'])
def take_book(request, library_id, book_id):
    book_info = requests.post(f"http://{REPORT_URL}/user/take", cookies=request.COOKIES)
    # todo check code

    # find LibraryBook then check count
    data = auth(request)

    try:
        library_book = LibraryBook.objects.get(library_id=library_id, book_id=book_id)
    except LibraryBook.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if library_book.count <= 0:
        return Response(status=status.HTTP_200_OK)
        # return response что нет книг(

    control_response = requests.post(f"http://{CONTROL_URL}/take", cookies=request.COOKIES)


    taken_book = TakenBook()
    taken_book.book_id = book_id
    taken_book.user_id = data['user_id']

    now_date = datetime.datetime.now(tz_MOS)
    added_seconds = datetime.timedelta(0, 25)
    expire_date = now_date + added_seconds
    taken_book.expire_date = expire_date

    taken_book.save()

    # todo post to report service taked genre of book

    library_book.count -= 1
    library_book.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_library(request, library_id):
    try:
        library = Library.objects.get(pk=library_id)
    except Library.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = LibrarySerializer(library)
    return Response(serializer.data)


@api_view(['POST'])
def return_book(request, library_id, book_id):
    data = auth(request)

    try:
        library_book = LibraryBook.objects.get(library_id=library_id, book_id=book_id)
    except LibraryBook.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        taken_book = TakenBook.objects.get(book_id=book_id, user_id=data['user_id'])
        now = datetime.datetime.now(tz_MOS)
        control_response = requests.post(f"http://{CONTROL_URL}/return", cookies=request.COOKIES)

        if taken_book.expire_date > now:
            rating_response = requests.post(f"http://{RATING_URL}/up", cookies=request.COOKIES)
            control_response = requests.post(f"http://{CONTROL_URL}/up", cookies=request.COOKIES)

            report_response = requests.post(f"http://{REPORT_URL}/user/in_time", cookies=request.COOKIES)
        else:
            rating_response = requests.post(f"http://{RATING_URL}/down", cookies=request.COOKIES)

            report_response = requests.post(f"http://{REPORT_URL}/user/expire", cookies=request.COOKIES)
        taken_book.delete()
    except LibraryBook.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    library_book.count += 1
    library_book.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_taken_books(request):
    is_authenticated, request, session = cookies(request)

    data = auth(request)
    user_id = data['user_id']

    books = list(TakenBook.objects.filter(user_id=user_id).values('book_id'))
    book_infos = []
    for book in books:
        service_response = requests.get(f"http://{BOOK_URL}/api/v1/book/{book['book_id']}")
        if service_response.status_code == status.HTTP_404_NOT_FOUND:
            continue
        book_info = service_response.json()
        book_infos.append(book_info)

    # books = list(LibraryBook.objects.filter(library_id=library_id).values_list('book_id', flat=True))
    # book_infos = []
    # for book_id in books:
    #     book = requests.get(f"http://{BOOK_URL}/api/v1/book/{book_id}").json()
    #     book_infos.append(book)

    # books = list(LibraryBook.objects.filter(library_id=library_id).values('book_id', 'count'))
    # book_infos = []
    # for book in books:
    #     book_info = requests.get(f"http://{BOOK_URL}/api/v1/book/{book['book_id']}").json()
    #     book_info['count'] = book['count']
    #     book_infos.append(book)
    # return Response(book_infos)
    return Response(book_infos)
