import datetime
import jwt
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.response import Response
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer
from session_service.settings import SECRET_KEY


@api_view(['POST'])
def register(request):
    if 'role' not in request.data:
        request.data.update({'role': 'user'})
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):

    try:
        username = request.data['username']
        password = request.data['password']
    except KeyError:
        raise ValidationError('Incorrect data')

    user = User.objects.filter(username=username).first()

    if user is None:
        raise AuthenticationFailed('User not found!')

    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect password!')

    payload = {
        'user_id': str(user.id),
        'username': str(username),
        'library_id': user.library_id,
        'role': str(user.role),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=9000000000),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'detail': 'Authenticated'
    }
    return response


@api_view(['GET'])
def validate(request):
    token = request.COOKIES.get('jwt')

    if token is None:
        return JsonResponse({'detail': 'Null token'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    except jwt.DecodeError:
        return JsonResponse({'detail': 'Null token'}, status=status.HTTP_401_UNAUTHORIZED)

    response = JsonResponse({'detail': 'Authenticated'}, status=status.HTTP_200_OK)
    response.set_cookie(key='jwt', value=token, httponly=True)
    return response


@api_view(['POST'])
def logout(request):
    try:
        data = auth(request)
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'detail': 'success',
            'user_id': data['user_id']
        }
        return response
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


# subsidiary
def auth(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
    # payload.pop('exp')
    # payload.pop('iat')
    return payload
