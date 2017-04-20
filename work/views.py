from django.shortcuts import render
from django.http import Http404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from customer.models import Address, Customer

from image.models import Image

from work.serializers import WorkDTOSerializer, DetailWorkSerializer
from work.models import Work

from worktype.models import WorkType

from worker.models import Worker

from customer.permissions import IsOwnerOrReadOnly

from .tasks import create_work as create_work_async
from .serializers import DetailWorkSerializer, DetailWorkDTOSerializer

import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def create_work(request):
    logger.info("creating work ...")
    serializer = WorkDTOSerializer(data = request.data)
    if request.method == 'GET':
        return Response(status = status.HTTP_400_BAD_REQUEST)
    try:
        if serializer.is_valid():
            worktype = WorkType.objects.filter(id = serializer.data['worktypeid']).first()
            date = serializer.data['date']
            if(serializer.data.get('description', None) != None):
                description = serializer.data['description']
            else:
                description = ''
            address = Address.objects.filter(id = serializer.data['addressid']).first()
            user = request.user
            customer = Customer.objects.filter(user__id__exact = user.id).first()
            work = Work(worktype = worktype, customer = customer, 
                        address = address, time = date, 
                        description = description)
            if serializer.data.get('asap', None) != None:
                work.asap = serializer.data['asap']
            work.save()
            logger.info('work created for customer ' + user.username)
            if(serializer.data.get('images', None) != None):
                for image in serializer.data['images']:
                    image = Image.objects.filter(id = image).first()
                    image.work = work
                    image.save()
                work.images = Image.objects.filter(pk__in = map(int, serializer.data['images']))
                logger.info('added images for created work')
            else:
                work.images = []
            serializer = DetailWorkSerializer(work)
            try:
                create_work_async.delay(work.id)
                logger.info('succesfully created work for customer ' + user.username)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            except:
                logger.error('queue not found')
                return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
    except WorkType.DoesNotExist:
        logger.error('created work for a worktype that does not exist')
        return Response(status = status.HTTP_400_BAD_REQUEST)
    except Address.DoesNotExist:
        logger.error('created work for a non existent address')
        return Response(status = status.HTTP_400_BAD_REQUEST)

class WorkDetail(APIView):
    """
        Retrieve, update or delete a customer instance.
    """
    permission_classes = ( IsOwnerOrReadOnly, )

    def get_object(self, pk):
        try:
            return Work.objects.get(pk = pk)
        except Work.DoesNotExist:
            raise Http404

    def put(self, request, pk, format = None):
        work = self.get_object(pk)
        self.check_object_permissions(self.request, work)
        serializer = DetailWorkDTOSerializer(data=request.data)
        if serializer.is_valid():
            description = serializer.data['description']
            work.description = description
            for image in serializer.data['images']:
                image = Image.objects.filter(id = image).first()
                image.work = work
                image.save()
            work.save()

            images = Image.objects.filter(work__id__exact = work.id)
            work.images = images
            # setting the worker to the work
            if work.worker is not None:
                worker = Worker.objects.get(pk = work.worker.id)
                work.worker = worker
            serializer = DetailWorkSerializer(work)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None):
        try:
            customer = Customer.objects.filter(user = request.user).first()
            work = Work.objects.get(pk = pk)
            if work.customer is None:
                return Response(status = status.HTTP_403_FORBIDDEN)

            if work.customer.id == customer.id:
                work.state = 'CANCELED'
                work.save()
                return Response(status = status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_403_FORBIDDEN)
        except Customer.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        except Work.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_my_works(request):
    user = request.user
    customer = Customer.objects.filter(user__id__exact = user.id).first()
    works = Work.objects.filter(customer__id__exact = customer  .id)
    state = request.query_params.get('state', None)
    if state is not None: # query has state filter
        statesList = state.split(',')
        works = works.filter(state__in = statesList)
    works = works.order_by('time', '-id').all()
    my_works = []
    for work in works:
        #setting images to fworker
        images = Image.objects.filter(work__id__exact = work.id)
        work.images = images
        # setting the worker to the work
        if work.worker is not None:
            worker = Worker.objects.get(pk = work.worker.id)
            work.worker = worker
        my_works.append(work)


    serializer = DetailWorkSerializer(data = my_works, many = True)
    if serializer.is_valid() == False:
        return Response(serializer.data)
    else:
        return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def assign_work(request, workid):
    return Response(status = status.HTTP_501_NOT_IMPLEMENTED)



