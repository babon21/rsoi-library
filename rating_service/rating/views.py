import jwt
from rest_framework import status
from rest_framework.decorators import api_view
from rating_service.settings import JWT_KEY
from rest_framework.response import Response

from .models import Rating
from .serializers import RatingSerializer


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
def up(request):
    data = auth(request)
    user_id = data['user_id']
    try:
        rating = Rating.objects.get(user_id=user_id)
        rating.rating += 10
    except Rating.DoesNotExist:
        rating = Rating()
        rating.user_id = user_id
        rating.rating = 10

    rating.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def down(request):
    data = auth(request)
    user_id = data['user_id']
    try:
        rating = Rating.objects.get(user_id=user_id)
        rating.rating -= 10
    except Rating.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    rating.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_rating(request):
    data = auth(request)
    user_id = data['user_id']
    try:
        rating = Rating.objects.get(user_id=user_id)
    except Rating.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = RatingSerializer(rating)
    return Response(serializer.data)
