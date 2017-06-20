from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from worktype.models import Category, WorkType

class WorkTypeList(ListView):
    model = Category


def landing(request):
    return render(request, 'landing.html')


