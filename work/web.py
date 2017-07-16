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
    try:
        work = Work.objects.get(pk = pk)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        p = canvas.Canvas(response)
        p.setLineWidth(.3)
        p.setFont('Helvetica', 12)
        
        p.drawString(30,750,'Recibo de Pago')
        p.drawString(30,735,'FixIt Group S.A.S')
        p.drawString(500,750, work.time.strftime("%Y-%m-%d"))
        p.line(480,747,580,747)
        
        p.drawString(275,725,'Costo total:')
        p.drawString(500,725,"$1,000.00")
        p.line(378,723,580,723)
        
        p.drawString(30,703,'Recibo a:')
        p.line(120,700,580,700)
        p.drawString(120,703,work.customer.user.get_full_name())

        p.showPage()
        p.save()
        return response
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
