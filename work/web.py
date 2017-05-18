from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from datetime import datetime

from customer.models import Customer, Address
from work.forms import WorkForm
from work.models import Work
from worktype.models import WorkType

def schedule_work_view(request, url_name):
    if request.method == 'GET':
      try:
          workType = WorkType.objects.get(url_name = url_name)
      except WorkType.DoesNotExist:
          raise Http404("WorkType does not exist")
      
      customer = Customer.objects.filter(user__id__exact = request.user.id).first()
      addresses = Address.objects.filter(customer__id__exact = customer.id)

      return render(
          request,
          'schedule_work.html',
          context = { 'worktype' : workType, 'myAddresses': addresses }
      )
    elif request.method == 'POST':
      if request.user is None:
        # TODO (): do login first
        return Response(status = status.HTTP_403_FORBIDDEN)

      worktypeId = request.POST.get('worktypeId');
      worktype = WorkType.objects.filter(id = worktypeId).first()
      customer = Customer.objects.filter(user__id__exact = request.user.id).first()

      form = WorkForm(request.POST)
      if form.is_valid():
        addressId = form.cleaned_data['addressId']
        date = form.cleaned_data['date']
        time = form.cleaned_data['time']
        
        dateTime = datetime.combine(date, time)
        address = Address.objects.filter(id = addressId).first()

        print(dateTime)
        work = Work(worktype = worktype, customer = customer, 
                    address = address, time = dateTime)
        work.save()
        return render(request, 'confirmation.html', {'form': form, 'work': work })
      else:
        addresses = Address.objects.filter(customer__id__exact = customer.id)
        return render(request, 'schedule_work.html', { 'worktype' : worktype, 'myAddresses': addresses, })