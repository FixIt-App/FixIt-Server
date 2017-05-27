from django.http import HttpResponse
from django.views.generic import ListView
from worktype.models import Category, WorkType

class WorkTypeList(ListView):
    model = Category
