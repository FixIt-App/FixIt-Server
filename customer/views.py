from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from customer.serializers import CustomerSerializer
from customer.models import Customer

# It seems that two class based views is the best option
class CustomerList(APIView):
    """
        List all customers or create new customer endpoint
    """
    def get(self, request, format = None):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            user = User(first_name = serializer.data['first_name'], \
                        last_name = serializer.data['last_name'],   \
                        username = serializer.data['username'],     \
                        email = serializer.data['email'])
            user.save()
            customer = Customer(user = user, city = serializer.data['city'])
            customer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    """
        Retrieve, update or delete a customer instance.
    """
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk = pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format = None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk, format = None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            user = customer.user
            user.first_name = serializer.data['first_name']
            user.last_name = serializer.data['last_name']
            user.email = serializer.data['email']
            user.save()
            customer.city = serializer.data['city']
            customer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

