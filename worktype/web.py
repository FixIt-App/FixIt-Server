from django.http import HttpResponse
from django.views.generic import ListView
from worktype.models import Category, WorkType
from django.shortcuts import render
from django.http import Http404

from customer.models import Customer, Address

class WorkTypeList(ListView):
    model = Category

def shedule_work_view(request, url_name):
    try:
        workType = WorkType.objects.get(url_name = url_name)
    except WorkType.DoesNotExist:
        raise Http404("WorkType does not exist")
    
    customer = Customer.objects.filter(user__id__exact = request.user.id).first()
    addresses = Address.objects.filter(customer__id__exact = customer.id)

    return render(
        request,
        'worktype/shedule_work.html',
        context = { 'worktype' : workType, 'myAddresses': addresses }
    )
