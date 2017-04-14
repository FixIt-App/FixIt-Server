from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse

from random import randint
import uuid



from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from customer.serializers import CustomerSerializer, AddressSerializer, PhoneConfirmationSerializer, ConfirmationSerializer
from customer.models import Customer, Address, Confirmation
from customer.permissions import IsOwnerOrReadOnly
from customer.tasks import confirm_user, confirm_email as confirm_email_async
from rest_framework import permissions
from django.db import transaction

# It seems that two class based views is the best option
class CustomerList(APIView):

    permission_classes = (permissions.AllowAny, )

    """
        List all customers or create new customer endpoint
    """
    def get(self, request, format = None):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many = True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, format = None):
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            user = User(first_name = serializer.data['first_name'], \
                        last_name = serializer.data['last_name'],   \
                        username = serializer.data['username'],     \
                        email = serializer.data['email'])
            user.set_password(serializer.data['password'])
            user.save()
            customer = Customer(user = user, city = serializer.data['city'], phone = serializer.data['phone'])
            customer.save()
            self.create_confirmations(customer)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def create_confirmations(self, customer):
        # SMS confirmation
        code = str(randint(100,999))
        sms_confirmation = Confirmation(
            customer = customer,
            code = code,
            confirmation_type = 'SMS'
        )
        
        sms_confirmation.save()
    
        # Email confirmation
        e_code = uuid.uuid4()
        mail_confirmation = Confirmation(
            customer = customer,
            code = e_code,
            confirmation_type = 'MAIL'
        )
        mail_confirmation.save()
        print("Sending confirmation sms to ... " + customer.phone)
        confirm_user.delay(customer.phone, code)
        print("Sending email confirmation to " + customer.user.email)
        confirm_email_async.delay(customer.user.email, e_code)


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
            customer = Customer.objects.filter(user__id__exact=request.user.id).first()
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
        customer.confirmations = Confirmation.objects.filter(customer__id = customer.id)
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

@api_view(['POST'])
def confirm_phone(request):
    try:
        if request.user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        customer = Customer.objects.filter(user__id__exact = user.id).first()
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_403_FORBIDDEN)
        

    serializer = PhoneConfirmationSerializer(data = request.data)
    try:
        serializer.is_valid()
        confirmation = Confirmation.objects.get(code = serializer.data['code'], customer = customer)
        confirmation.state = True
        confirmation.save()
        return Response(status=status.HTTP_200_OK)
    except Confirmation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def my_confirmation(request):
    user = request.user
    customer = Customer.objects.filter(user__id__exact = user.id).first()
    confimation = Confirmation.objects.filter(customer = customer)
    serializer = ConfirmationSerializer(data = confimation, many = True)
    serializer.is_valid()
    return Response(serializer.data)



def confirm_email(request, code):
    try:
        confirmation = Confirmation.objects.get(code = code)
        confirmation.state = True
        confirmation.save()
        return HttpResponse("Ya confirmaste tu correo. Muchas gracias")
    except Confirmation.DoesNotExist:
         raise Http404("Confirmation not exist")

@api_view(['GET'])
def resend_sms_code(request):
    try:
        if request.user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        customer = Customer.objects.filter(user__id__exact = user.id).first()
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_403_FORBIDDEN)

    confimations = Confirmation.objects.filter(customer = customer).all()
    for confirmation in confimations:
        if confirmation.confirmation_type == 'SMS':
            print("Sending confirmation sms to ... " + customer.phone)
            confirm_user.delay(customer.phone, confirmation.code)
            return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
    

