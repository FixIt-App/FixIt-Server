from rest_framework import serializers
from work.dto import WorkDTO

class StringListField(serializers.ListField):
    child = serializers.CharField()

class WorkDTOSerializer(serializers.Serializer):
    worktypeid = serializers.IntegerField()
    date = serializers.DateTimeField()
    description = serializers.CharField(max_length = 500)
    addressid = serializers.IntegerField()
    images = StringListField()
