from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import NotificationToken
from .serializers import TokenSerializer

@api_view(['POST'])
def register_device(request):
    if request.user is None:
        return Response(status = status.HTTP_401_UNAUTHORIZED)
    serializer = TokenSerializer(data = request.data)
    if serializer.is_valid() == False:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    try:
        token = NotificationToken.objects.get(token = serializer.data['token'])
        return Response(status = status.HTTP_200_OK) 
    except NotificationToken.DoesNotExist:
        new_token = NotificationToken(user = request.user, 
                                    token = serializer.data['token'],
                                    platform_type = serializer.data['platform_type'],
                                    token_type = serializer.data['token_type'])
        try:
            new_token.save()
            return Response(status = status.HTTP_201_CREATED) 
        except:
            return Response(status = status.HTTP_400_BAD_REQUEST) 

@api_view(['DELETE'])
def remove_device_token(request):
    if request.user is None:
        return Response(status = status.HTTP_401_UNAUTHORIZED)
    serializer = TokenSerializer(data = request.data)
    if serializer.is_valid() == False:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    try:
        token = NotificationToken.objects.get(token = serializer.data['token'])
        token.delete()
        return Response(status = status.HTTP_200_OK) 
    except NotificationToken.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND) 


