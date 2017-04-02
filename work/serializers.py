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
    description = serializers.CharField(max_length = 500)
    addressid = serializers.IntegerField()
    images = StringListField()


class DetailWorkSerializer(serializers.Serializer):
    images = ImageSerializer(many = True)
    worktype = WorkTypeSerializer()
    address = AddressSerializer()
    id = serializers.IntegerField()
    description = serializers.CharField()
