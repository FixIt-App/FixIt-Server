from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from image.serializers import ImageSerializer

class ImageUploadView(APIView):

    def post(self, request, format=None):
        serializer = ImageSerializer(data = request.data)
        user = request.user
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)