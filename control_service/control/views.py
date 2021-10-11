from django.shortcuts import render

# Create your views here.
import jwt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from control_service.settings import JWT_KEY
from .models import UserMonitoring

from .serializers import MonitoringSerializer


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
def take_book(request):
    data = auth(request)
    user_id = data['user_id']
    try:
        monitoring = UserMonitoring.objects.get(user_id=user_id)
        if monitoring.max_count > monitoring.current_count:
            monitoring.current_count += 1

    except UserMonitoring.DoesNotExist:
        monitoring = UserMonitoring()
        monitoring.user_id = user_id
        monitoring.max_count = 2
        monitoring.current_count = 1

    monitoring.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def return_book(request):
    data = auth(request)
    user_id = data['user_id']
    try:
        monitoring = UserMonitoring.objects.get(user_id=user_id)
        monitoring.current_count -= 1

    except UserMonitoring.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    monitoring.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_monitoring(request):
    data = auth(request)
    user_id = data['user_id']
    try:
        monitoring = UserMonitoring.objects.get(user_id=user_id)
    except UserMonitoring.DoesNotExist:
        monitoring = UserMonitoring()
        monitoring.user_id = user_id
        monitoring.max_count = 3
        monitoring.current_count = 0
        monitoring.save()

    serializer = MonitoringSerializer(monitoring)
    return Response(serializer.data)


@api_view(['POST'])
def up(request):
    data = auth(request)
    user_id = data['user_id']
    try:
        rating = UserMonitoring.objects.get(user_id=user_id)
        rating.max_count += 1
    except UserMonitoring.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    rating.save()
    return Response(status=status.HTTP_200_OK)
