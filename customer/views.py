from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets

from customer.serializers import CustomerSerializer
# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    """
        Api endpoint that lets customers be created
    """
    queryset = User.objects.all()
    serializer_class = CustomerSerializer
