from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from customer.serializers import CustomerSerializer
# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    """
        Api endpoint that lets customers be created
    """
    queryset = User.objects.all()
    serializer_class = CustomerSerializer

@api_view(['GET'])
def get_all_customers(request):
    """
        Lists All Customers, or add customer
    """
    if request.method == 'POST':
        return add_customer(request)

    customers = User.objects.all()
    serializer = CustomerSerializer(customers, many = True)
    return Response(serializer.data)



# Class based views, por ahora es como una mejor aproximación
class CustomerList(APIView):
    """
        List all customers or create new customer endpoint
    """
    def get(self, request, format = None):
        customer = User.objects.call()
        serializer = CustomerSerializer(customers, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(erializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    """
        Retrieve, update or delete a customer instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = CustomerSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

