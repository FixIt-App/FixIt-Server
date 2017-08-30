from rest_framework import serializers

from work.dto import WorkDTO
from work.models import Work

from customer.serializers import AddressSerializer

from worktype.serializers import WorkTypeSerializer

from worker.serializers import WorkerSerializer

from image.serializers import ImageSerializer, ImageDTOSerializer

class StringListField(serializers.ListField):
    child = serializers.CharField()

class WorkDTOSerializer(serializers.Serializer):
    worktypeid = serializers.IntegerField()
    date = serializers.DateTimeField()
    description = serializers.CharField(max_length = 500, required = False)
    addressid = serializers.IntegerField()
    images = StringListField(required = False)
    asap = serializers.BooleanField(required = False)


class DetailWorkSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField()
    time = serializers.DateTimeField()
    images = ImageDTOSerializer(many = True, required = False)
    worktype = WorkTypeSerializer()
    address = AddressSerializer()
    state = serializers.CharField()
    worker = WorkerSerializer(required = False)
    

class DetailWorkDTOSerializer(serializers.Serializer):
    description = serializers.CharField()
    images = StringListField()

class PriceSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2)

class RatingDTOSerializer(serializers.Serializer):
    work_id = serializers.IntegerField()
    score = serializers.IntegerField()
    comment = serializers.CharField(max_length = 500, required = False)
