from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from quickstart.serializers import UserSerializer, GroupSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
        Api endpoint that allows users to be created
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = GroupSerializer
