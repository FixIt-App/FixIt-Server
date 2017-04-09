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
from .serializers import DetailWorkSerializer

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

@api_view(['GET'])
def get_my_works(request):
    user = request.user
    customer = Customer.objects.filter(user__id__exact = user.id).first()
    works = Work.objects.filter(customer__id__exact = customer.id)
    state = request.query_params.get('state', None)
    if state is not None: # query has state filter
        works = works.filter(state = state)
    works = works.order_by('+time', '-id').all()
    my_works = []
    for work in works:
        images = Image.objects.filter(work__id__exact = work.id)
        work.images = images
        my_works.append(work)
    serializer = DetailWorkSerializer(data = my_works, many = True)
    if serializer.is_valid() == False:
        return Response(serializer.data)
    else:
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR) 
    



    
