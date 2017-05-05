from django.http import HttpResponse
from django.views.generic import ListView
from worktype.models import Category

class WorkTypeList(ListView):
    model = Category
