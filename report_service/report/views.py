import jwt
import requests
from rest_framework import status, filters
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from report_service.settings import JWT_KEY


from .models import GenreStat, UserStat
from .serializers import GenreStatSerializer, UserStatSerializer

BOOK_URL = "127.0.0.1:9002/api/v1/book"


def auth(request):
    token = request.COOKIES.get('jwt')

    if not token:
        return
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=['HS256'], options={"verify_exp": False})
    except jwt.DecodeError:
        return None
    return payload


@api_view(['POST'])
def update_stat(request, book_id):
    response = requests.get(f"http://{BOOK_URL}/{book_id}")
    book = response.json()
    genre = book['genre']

    try:
        stat = GenreStat.objects.get(genre=genre)
        stat.count += 1
    except GenreStat.DoesNotExist:
        stat = GenreStat()
        stat.genre = genre
        stat.count = 1

    stat.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def genre_stat(request):
    serializer = GenreStatSerializer(GenreStat.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class GenreListView(ListAPIView):
    queryset = GenreStat.objects.all()
    serializer_class = GenreStatSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['count']
    ordering = ['-count']


@api_view(['GET'])
def user_stat(request):
    # all = UserStat.objects.all().count()
    serializer = UserStatSerializer(UserStat.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def take_stat(request):
    data = auth(request)
    user_id = data['user_id']
    try:
        stat = UserStat.objects.get(user_id=user_id)
        stat.taken_count += 1
    except UserStat.DoesNotExist:
        stat = UserStat()
        stat.user_id = user_id
        stat.taken_count = 1
        stat.in_time = 0
        stat.expired_count = 0

    stat.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def expire_stat(request):
    data = auth(request)
    user_id = data['user_id']
    try:
        stat = UserStat.objects.get(user_id=user_id)
    except UserStat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    stat.expired_count += 1
    stat.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def in_time_stat(request):
    data = auth(request)
    user_id = data['user_id']
    try:
        stat = UserStat.objects.get(user_id=user_id)
    except UserStat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    stat.in_time += 1
    stat.save()
    return Response(status=status.HTTP_200_OK)
