from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from customer.serializers import CustomerSerializer
# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    """
        Api endpoint that lets customers be created
    """
    queryset = User.objects.all()
    serializer_class = CustomerSerializer

@api_view(['GET'])
def get_all_customers(request):
    """
        Lists All Customers
    """
    customers = User.objects.all()
    serializer = CustomerSerializer(customers, many = True)
    return Response(serializer.data)

