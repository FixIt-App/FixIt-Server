from rest_framework import serializers

from work.dto import WorkDTO
from work.models import Work

from customer.serializers import AddressSerializer

from worktype.serializers import WorkTypeSerializer

from image.serializers import ImageSerializer

class StringListField(serializers.ListField):
    child = serializers.CharField()

class WorkDTOSerializer(serializers.Serializer):
    worktypeid = serializers.IntegerField()
    date = serializers.DateTimeField()
    description = serializers.CharField(max_length = 500, required = False)
    addressid = serializers.IntegerField()
    images = StringListField(required = False)


class DetailWorkSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField()
    time = serializers.DateTimeField()
    images = ImageSerializer(many = True)
    worktype = WorkTypeSerializer()
    address = AddressSerializer()
    state = serializers.CharField()

class DetailWorkDTOSerializer(serializers.Serializer):
    description = serializers.CharField()
    images = StringListField()
