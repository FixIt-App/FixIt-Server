from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from reportlab.platypus.paragraph import Paragraph
from  reportlab.lib.styles import ParagraphStyle as PS

from datetime import datetime

from customer.models import Customer, Address
from work.forms import WorkForm
from work.models import Work
from worktype.models import WorkType
from work.business_logic import create_work_and_enqueue
from work.services import calculate_price


def generate_invoice(request, pk):
    try:
        work = Work.objects.get(pk = pk)
        asap = 'false'
        if work.asap is True:
            asap = 'true'
        pricing = calculate_price(work.worktype.id, asap, work.time)
        print(str(pricing))
        return render(request, 'emails/invoice.html', {'work': work, 'pricing': pricing})
    except Work.DoesNotExist:
        return Http404('Work does not exist')

def schedule_work_view(request, url_name):
    if request.method == 'GET':
      try:
          if request.user.id is None:
              messages.warning(request, 'Por favor inicia sesión antes de pedir un trabajo.')
              return redirect('login')
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
        return Response(status = status.HTTP_403_FORBIDDEN)

      worktypeId = request.POST.get('worktypeId')
      worktype = WorkType.objects.filter(id = worktypeId).first()
      customer = Customer.objects.filter(user__id__exact = request.user.id).first()

      form = WorkForm(request.POST)
      if form.is_valid():
        addressId = form.cleaned_data['addressId']
        date = form.cleaned_data['date']
        # TODO(a-santamaria): utc -5
        dateTime = datetime.strptime(date, "%Y/%m/%d %H:%M")
        address = Address.objects.filter(id = addressId).first()
        createdWork = create_work_and_enqueue(worktype = worktype, customer = customer, 
                                            address = address, time = dateTime,
                                            description = '', asap = False, images = [])
        return render(request, 'confirmation.html', {'work': createdWork })
      else:
        addresses = Address.objects.filter(customer__id__exact = customer.id)
        return render(request, 'schedule_work.html', { 'worktype' : worktype, 'myAddresses': addresses, })
