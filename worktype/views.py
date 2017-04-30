from django.shortcuts import render
from django.http import Http404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from worktype.models import WorkType, Category
from worktype.serializers import WorkTypeSerializer, CategoryListSerializer

from django.shortcuts import render

class WorkTypeList(APIView):
    """
        List all worktypes or create new worktype
    """

    def get(self, request, format = None):
        worktypes = WorkType.objects.all()
        serializers = WorkTypeSerializer(worktypes, many = True)
        return Response(serializers.data)

    def post(self, request, format = None):
        """
            Not supported yet
        """
        return Response(serializer.errors, status = status.HTTP_501_NOT_IMPLEMENTED)



class CategoryList(APIView):

    def get(self, request, format = None):
        categories = Category.objects.order_by('-order').all()
        serializers = CategoryListSerializer(categories, many = True)
        return Response(serializers.data)

    def post(self, request, format = None):
        """
            Not supported yet
        """
        return Response(serializer.errors, status = status.HTTP_501_NOT_IMPLEMENTED)



def web_get_works(request):
    context = {'worktypes': []}
    return render(request, 'works.html', context)
