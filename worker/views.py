from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from image.models import Image

from work.models import Work
from work.serializers import DetailWorkSerializer

from worker.models import Worker
    
