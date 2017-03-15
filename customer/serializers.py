from customer.models import Customer, Address
from django.contrib.auth.models import User
from rest_framework import serializers

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """
        Customer serializer class 
        The base model is user for easier serialization
    """
    username = serializers.CharField(source = 'user.username')
    first_name = serializers.CharField(source = 'user.first_name')
    last_name = serializers.CharField(source = 'user.last_name')
    email = serializers.CharField(source = 'user.email')

    class Meta:
        model = Customer
        fields  = fields = ('id', 'username', 'first_name', 'last_name', 'email', 'city')


class AddressSerializer(serializers.ModelSerializer):
    """
        Address serializer class
    """
    class Meta:
        model = Address
        fields  = fields = ('id', 'name', 'address',  'city', 'country')