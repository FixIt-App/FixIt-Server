from customer.models import Customer
from django.contrib.auth.models import User
from rest_framework import serializers

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """
        Customer serializer class 
        The base model is user for easier serialization
    """
    city = serializers.CharField(source = 'customer.city')

    class Meta:
        model = User
        fields  = fields = ('id', 'username',  'first_name', 'last_name', 'email', 'city')
