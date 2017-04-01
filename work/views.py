from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from customer.models import Address, Customer

from image.models import Image

from work.serializers import WorkDTOSerializer
from worktype.models import WorkType
from work.models import Work

from .tasks import create_work as create_work_async

@api_view(['POST'])
def create_work(request):
    serializer = WorkDTOSerializer(data = request.data)
    if request.method == 'GET':
        return Response(status = status.HTTP_400_BAD_REQUEST)
    try:
        if serializer.is_valid():
            worktype = WorkType.objects.filter(id = serializer.data['worktypeid']).first()
            date = serializer.data['date']
            description = serializer.data['description']
            address = Address.objects.filter(id = serializer.data['addressid']).first()
            user = request.user
            customer = Customer.objects.filter(user__id__exact = user.id).first()
            work = Work(worktype = worktype, customer = customer, 
                        address = address, time = date, 
                        description = description)
            work.save()
            for image in serializer.data['images']:
                image = Image.objects.filter(id = image).first()
                image.work = work
                image.save()
            
            create_work_async.delay(work.id)
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
    except WorkType.DoesNotExist:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    except Address.DoesNotExist:
        return Response(status = status.HTTP_400_BAD_REQUEST)

        
    

    
