from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.models import User

from customer.views import create_confirmations
from customer.models import Customer

import logging

logger = logging.getLogger(__name__)

def login(request):
    if request.user is not None:
        print("usuario"  + request.user.username)
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
            return render(request, 'login.html', context)
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
        
