from customer.models import Customer, Address, Confirmation
from django.contrib.auth.models import User
from rest_framework import serializers

class ConfirmationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Confirmation
        fields = ('confirmation_type', 'state')
        
class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """
        Customer serializer class 
        The base model is user for easier serialization
    """
    username = serializers.CharField(source = 'user.username', required = False)
    first_name = serializers.CharField(source = 'user.first_name', required = False)
    last_name = serializers.CharField(source = 'user.last_name', required = False)
    email = serializers.CharField(source = 'user.email', required = False)
    password = serializers.CharField(source = 'user.password', required = False)
    confirmations = ConfirmationSerializer(many = True, required = False)

    class Meta:
        model = Customer
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'city', 'password', 'phone', 'confirmations')

class CustomerConfigurationSerializer(serializers.ModelSerializer):
    """
        Customer serializer class 
        The base model is user for easier serialization
    """
    first_name = serializers.CharField(source = 'user.first_name', required = False)
    last_name = serializers.CharField(source = 'user.last_name', required = False)
    email = serializers.CharField(source = 'user.email', required = False)
    password = serializers.CharField(source = 'user.password', required = False)
    city = serializers.CharField(required = False)
    password = serializers.CharField(required = False)
    phone = serializers.CharField(required = False)
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'city', 'password', 'phone')

class AddressSerializer(serializers.ModelSerializer):
    """
        Address serializer class
    """
    latitude = serializers.FloatField(required = False)
    longitude = serializers.FloatField(required = False)

    class Meta:
        model = Address
        fields  = fields = ('id', 'name', 'address',  'city', 'country', 'latitude', 'longitude')


class PhoneConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField()

class TPagaTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()
