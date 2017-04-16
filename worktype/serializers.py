from worktype.models import WorkType, Category
from rest_framework import serializers

class WorkTypeSerializer(serializers.ModelSerializer):
    """
        WorkType serializers class
    """

    class Meta:
        model = WorkType
        fields = ('id', 'name', 'description', 'icon', 'price_type', 'price', 'order')


class CategoryListSerializer(serializers.HyperlinkedModelSerializer):

    worktypes = WorkTypeSerializer(many = True)

    class Meta:
        model = Category
        fields = ('name', 'worktypes', 'order')
