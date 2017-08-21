import dateutil
import decimal

import os

from sendgrid.helpers.mail import *
import sendgrid

from worktype.models import WorkType
from work.models import DynamicPricing


def calculate_price(worktypeid, asap, date):
    if worktypeid is None or asap is None or date is None:
        return None
    try:
        asap = asap.lower() in ('true', 'yes')
        worktype = WorkType.objects.get(pk = worktypeid)
        basePrice = worktype.price
        total = basePrice
        response = {}
        response['breakdown'] = []

        service = {}
        service['name'] = "Servicio"
        service['price'] = basePrice
        response['breakdown'].append(service)

        if asap is not None and asap is True:
            # defined price for asap services
            chargeAsap = {}
            chargeAsap['name'] = "Lo necesito ahora mismo"
            chargeAsap['price'] = basePrice * decimal.Decimal(0.5)
            response['breakdown'].append(chargeAsap) 
            total += basePrice * decimal.Decimal(0.5)

        work_date = date
        if work_date is None:
            return None
        dynamic_prices = DynamicPricing.objects.all()
        for dynamic in dynamic_prices:
            if in_between(work_date.time(), dynamic.start, dynamic.end):
                chargeOverNight = {}
                chargeOverNight['name'] = "Recargo nocturno"
                chargeOverNight['price'] = basePrice * (dynamic.multiplier - 1)
                response['breakdown'].append(chargeOverNight)
                total += basePrice * (dynamic.multiplier - 1)
                break

        taxIva = {}
        taxIva['name'] = "IVA (19%)"
        taxIva['price'] = total * decimal.Decimal(0.19)
        response['breakdown'].append(taxIva)

        response['total'] = total * decimal.Decimal(1.19)
        return response
    except WorkType.DoesNotExist:
        return None

def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else: # over midnight e.g., 23:30-04:15
        return start <= now or now < end


def send_email(from_email, to_email, subject, message):
    sent_to = to_email
    sg = sendgrid.SendGridAPIClient(apikey = os.environ.get('EMAIL_API_KEY'))
    from_email = Email(from_email)
    to_email = Email(to_email)
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print("se envio un correo a " + sent_to)
    print(response.status_code)
    print(response.body)
