from django.shortcuts import render, redirect

from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.models import User
from django.contrib import messages


from rest_framework import status
from customer.forms import AddressForm
from customer.serializers import AddressSerializer
from customer.models import Customer, Address

from customer.views import create_confirmations
import logging

logger = logging.getLogger(__name__)
def login(request):
    if request.method == 'GET':
        context = {'error': None}
        return render(request, 'login.html', context)
    else:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            django_login(request, user)
            context = {}
            return redirect('works')
        else:
            logout(request)
            context = {'error': True}
            return render(request, 'login.html', context)

def sign_up(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'signup.html', context)
    else:
        print("Post request to create user")
        logger.info('Creating user %s started' % request.POST.get('username', None))
        user = User(first_name = request.POST.get('first_name', None), \
                    last_name = request.POST.get('last_name', None),   \
                    username = request.POST.get('username', None),     \
                    email = request.POST.get('username', None))
        user.set_password(request.POST.get('password', None))
        user.save()
        customer = Customer(user = user, city = 'Bogotá', phone=request.POST.get('phone', None))
        customer.save()
        create_confirmations(customer)
        django_login(request, user)
        return redirect('works')

def add_address(request):
    if request.method == 'POST':
         form = AddressForm(request.POST)
         if form.is_valid():
            customer = Customer.objects.filter(user__id__exact=request.user.id).first()
            address = Address(name = form.cleaned_data['name'], \
                        address = form.cleaned_data['address'], \
                        city = form.cleaned_data['city'],       \
                        country = form.cleaned_data['country'], \
                        customer = customer)
            address.save()
            serializer = AddressSerializer(address)
            context = {}
            url_name = request.POST.get('url_name')
            return redirect('schedule-work', url_name = url_name)
    context = {}
    return render(request, 'signup.html', context)
