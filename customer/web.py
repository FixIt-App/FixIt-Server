from django.shortcuts import render
from django.http import Http404
from django.contrib.auth import authenticate, login as django_login, logout

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
    context = {}
    return render(request, 'signup.html', context)
