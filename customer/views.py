from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.db import transaction

from random import randint
import uuid

import logging

logger = logging.getLogger(__name__)

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from payments.tpaga import create_customer as create_customer_tpaga, associate_credit_card, get_credit_card_data

from customer.serializers import CustomerSerializer, CustomerConfigurationSerializer, AddressSerializer, PhoneConfirmationSerializer, ConfirmationSerializer, TPagaTokenSerializer
from customer.models import Customer, Address, Confirmation, TPagaCustomer
from customer.permissions import IsOwnerOrReadOnly
from customer.tasks import confirm_user, confirm_email as confirm_email_async
from customer.services import create_confirmations


# It seems that two class based views is the best option
class CustomerList(APIView):

    permission_classes = (permissions.AllowAny, )

    """
        List all customers or create new customer endpoint
    """
    def get(self, request, format = None):
        logger.info('get all customers endpoint')
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many = True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, format = None):
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            logger.info('Creating user %s started' % serializer.data['username'])
            user = User(first_name = serializer.data['first_name'], \
                        last_name = serializer.data['last_name'],   \
                        username = serializer.data['username'],     \
                        email = serializer.data['email'])
            user.set_password(serializer.data['password'])
            user.save()
            customer = Customer(user = user, city = serializer.data['city'], phone = serializer.data['phone'])
            customer.save()
            create_confirmations(customer)
            create_customer_tpaga(user.email, user.first_name, user.last_name, customer.id, customer.phone)
            serializer = CustomerSerializer(customer)
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
        logger.info('Getting details from customer'  % customer.user.username)
        self.check_object_permissions(self.request, customer)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk, format = None):
        customer = self.get_object(pk)
        self.check_object_permissions(self.request, customer)
        serializer = CustomerConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            logger.info('Updating customer ' + customer.user.username)
            user = customer.user
            if serializer.data.get('first_name', None) != None and user.first_name != serializer.data['first_name']:
                user.first_name = serializer.data['first_name']
                user.save()

            if serializer.data.get('last_name', None) != None and user.last_name != serializer.data['last_name']:
                user.last_name = serializer.data['last_name']
                user.save()

            if serializer.data.get('email', None) != None and user.email != serializer.data['email']:
                if User.objects.filter(username=serializer.data['email']).count() > 0:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                user.email = serializer.data['email']
                user.username = serializer.data['email']
                customer = Customer.objects.filter(user = user).first()
                confirmation = Confirmation.objects.filter(customer = customer, confirmation_type = 'MAIL').first()
                customer.save()
                print("Sending email confirmation to " + user.email)
                confirm_email_async.delay(user.email, confirmation.code)

            if serializer.data.get('phone', None) != None and customer.phone != serializer.data['phone']:
                if Customer.objects.filter(phone=serializer.data['phone']).count() > 0:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                customer.phone = serializer.data['phone']
                confirmation = Confirmation.objects.filter(customer = customer, confirmation_type = 'SMS').first()
                customer.save()
                print("Sending confirmation sms to " + customer.phone)
                confirm_user.delay(customer.phone, confirmation.code)

            if serializer.data.get('password', None) != None:
                user.set_password(serializer.data['password'])
                user.save()

            if serializer.data.get('city', None) != None and customer.city != serializer.data['city']:
                customer.city = serializer.data['city']
                customer.save()

            
            sendSerializer = CustomerSerializer(customer)
            return Response(sendSerializer.data)
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
            
            if serializer.data.get('latitude', None) != None:
                address.latitude = serializer.data['latitude']

            if serializer.data.get('longitude', None) != None:
                address.longitude = serializer.data['longitude']

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
        logger.info('getting auth data for customer ' + customer.user.username)
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
        logger.info('getting all addresses from customer ' + customer.user.username)
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
        logger.info('Confirmed users phone ' + user.username)
        return Response(status=status.HTTP_200_OK)
    except Confirmation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def my_confirmation(request):
    user = request.user
    logger.info('getting al confirmations for ' +  user.username)
    customer = Customer.objects.filter(user__id__exact = user.id).first()
    confimation = Confirmation.objects.filter(customer = customer)
    serializer = ConfirmationSerializer(data = confimation, many = True)
    serializer.is_valid()
    return Response(serializer.data)



def confirm_email(request, code):
    try:
        logger.info('Confirmation for email with code ' +  code)
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

@api_view(['GET'])
def resend_verification_email(request):
    try:
        if request.user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        customer = Customer.objects.filter(user__id__exact = user.id).first()
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_403_FORBIDDEN)

    confimations = Confirmation.objects.filter(customer = customer).all()
    for confirmation in confimations:
        if confirmation.confirmation_type == 'MAIL':
            print("Sending confirmation email to ... " + customer.user.email)
            confirm_email_async.delay(customer.user.email, confirmation.code)
            return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def is_email_available(request, email):
    if not email or email == '':
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email = email).all()
    if not user:
        return Response(True, status=status.HTTP_200_OK)
    else:
        if request.user and request.user == user.first():
            return Response(True, status=status.HTTP_200_OK)
        else:
            return Response(False, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def is_phone_available(request, phone):
    if not phone or phone == '':
        return Response(status=status.HTTP_400_BAD_REQUEST)

    customer = Customer.objects.filter(phone = phone).first()
    if not customer:
        return Response(True, status=status.HTTP_200_OK)
    else:
        if request.user and request.user == customer.user:
            return Response(True, status=status.HTTP_200_OK)
        else:
            return Response(False, status=status.HTTP_200_OK)

@api_view(['POST'])
def save_payment_method_tpaga(request):
    serializer = TPagaTokenSerializer(data = request.data)
    if serializer.is_valid():
        user = request.user
        customer = Customer.objects.filter(user__id__exact = user.id).first()
        print(customer.id)
        tpagaCustomer = TPagaCustomer.objects.filter(customer__id__exact = customer.id).first()
        tpagaCustomer.token = serializer.data['token']
        tpagaCustomer.save()
        associate_credit_card(tpagaCustomer.tpaga_id, tpagaCustomer.token, tpagaCustomer)
        return Response(status = status.HTTP_201_CREATED )
    else:
        return Response(status = status.HTTP_400_BAD_REQUEST)


class TPagaPaymentDetail(APIView):
    """
        Retrieve, update or delete TPAGA data.
    """
    def get(self, request, format = None):
        try:
            user = request.user
            customer = Customer.objects.filter(user__id__exact = user.id).first()
            tpagaCustomer = TPagaCustomer.objects.filter(customer__id__exact = customer.id).first()
            if tpagaCustomer is None or tpagaCustomer.credit_card_id is None:
                return Response(status = status.HTTP_404_NOT_FOUND)
            return Response(get_credit_card_data(tpagaCustomer.tpaga_id, tpagaCustomer.credit_card_id), status = status.HTTP_200_OK)
        except (Customer.DoesNotExist, TPagaCustomer.DoesNotExist):
            return Response(status = status.HTTP_404_NOT_FOUND)

    def delete(self, request, format = None):
        try:
            user = request.user
            customer = Customer.objects.filter(user__id__exact = user.id).first()
            tpagaCustomer = TPagaCustomer.objects.filter(customer__id__exact = customer.id).first()
            if tpagaCustomer is None:
                return Response(status = status.HTTP_404_NOT_FOUND)
            tpagaCustomer.token = None;
            tpagaCustomer.credit_card_id = None;
            tpagaCustomer.save()
            return Response(status = status.HTTP_200_OK)
        except (Customer.DoesNotExist, TPagaCustomer.DoesNotExist):
            return Response(status = status.HTTP_404_NOT_FOUND)

