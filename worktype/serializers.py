from worktype.models import WorkType
from rest_framework import serializers

class WorkTypeSerializer(serializers.ModelSerializer):
    """
        WorkType serializers class
    """

    class Meta:
        model = WorkType
        fields = ('id', 'name', 'description', 'icon')



