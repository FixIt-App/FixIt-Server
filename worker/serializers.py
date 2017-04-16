
from worker.models import Worker
from django.contrib.auth.models import User
from rest_framework import serializers


class WorkerSerializer(serializers.HyperlinkedModelSerializer):
    """
        Customer serializer class 
        The base model is user for easier serialization
    """
    username = serializers.CharField(source = 'user.username')
    first_name = serializers.CharField(source = 'user.first_name')
    last_name = serializers.CharField(source = 'user.last_name')
    email = serializers.CharField(source = 'user.email')

    class Meta:
        model = Worker
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone', 'profile_pic', 'rh', 'document_id')

