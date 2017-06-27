from random import randint
import uuid
import logging
logger = logging.getLogger(__name__)

from customer.models import Confirmation
from customer.tasks import confirm_user, confirm_email as confirm_email_async

import logging

logger = logging.getLogger(__name__)

def create_confirmations(customer):
    # SMS confirmation
    code = str(randint(100,999))
    sms_confirmation = Confirmation(
        customer = customer,
        code = code,
        confirmation_type = 'SMS'
    )
    
    sms_confirmation.save()

    # Email confirmation
    e_code = uuid.uuid4()
    mail_confirmation = Confirmation(
        customer = customer,
        code = e_code,
        confirmation_type = 'MAIL'
    )
    mail_confirmation.save()
    logger.info("Sending confirmation sms to ... " + customer.phone)
    confirm_user.delay(customer.phone, code)
    logger.info("Sending email confirmation to " + customer.user.email)
    confirm_email_async.delay(customer.user.email, e_code)
