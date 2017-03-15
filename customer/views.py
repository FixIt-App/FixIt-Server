from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from customer.serializers import CustomerSerializer, AddressSerializer
from customer.models import Customer, Address
from customer.permissions import IsOwnerOrReadOnly

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
    permission_classes = ( IsOwnerOrReadOnly,)

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk = pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format = None):
        customer = self.get_object(pk)
        self.check_object_permissions(self.request, customer)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk, format = None):
        customer = self.get_object(pk)
        self.check_object_permissions(self.request, customer)
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
        self.check_object_permissions(self.request, customer)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddressList(APIView):
    """
        List all customers or create new customer endpoint
    """
    def get(self, request, format = None):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = AddressSerializer(data = request.data)
        if serializer.is_valid():
            customer = Customer.objects.filter(user__id__iexact=request.user.id).first()
            address = Address(name = serializer.data['name'], \
                        address = serializer.data['address'], \
                        city = serializer.data['city'],       \
                        country = serializer.data['country'], \
                        customer = customer)
            address.save()
            serializer = AddressSerializer(address)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class AddressDetail(APIView):
    """
        Retrieve, update or delete a customer instance.
    """
    permission_classes = ( IsOwnerOrReadOnly,)

    def get_object(self, pk):
        try:
            return Address.objects.get(pk = pk)
        except Address.DoesNotExist:
            raise Http404

    def get(self, request, pk, format = None):
        address = self.get_object(pk)
        self.check_object_permissions(self.request, address)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def put(self, request, pk, format = None):
        address = self.get_object(pk)
        self.check_object_permissions(self.request, address)
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        address = self.get_object(pk)
        self.check_object_permissions(self.request, address)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_customer_authenticated(request):
    """
    Retrieve customer instance given the auth token.
    """
    try:
        user = request.user
        customer = Customer.objects.filter(user__id__exact=user.id).first()
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)


@api_view(['GET'])
def get_customer_adresses(request):
    """
        Gets the user adresses
    """
    try:
        user = request.user
        customer = Customer.objects.filter(user__id__exact = user.id).first()
        addresses = Address.objects.filter(customer__id__exact = customer.id)
        serializer = AddressSerializer(addresses, many = True)
        return Response(serializer.data)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

