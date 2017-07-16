from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages

from reportlab.pdfgen import canvas

from datetime import datetime

from customer.models import Customer, Address
from work.forms import WorkForm
from work.models import Work
from worktype.models import WorkType
from work.business_logic import create_work_and_enqueue

def generate_invoice(request, pk):
    print('Entra')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    p = canvas.Canvas(response)
    p.drawString(0, 0, "Recibo de Pago FixIt.")
    p.showPage()
    p.save()
    return response

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
