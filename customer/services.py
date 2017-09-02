from random import randint
import uuid
import logging

logger = logging.getLogger(__name__)

from django.contrib.auth.models import User

from customer.models import Confirmation
from customer.tasks import confirm_user, confirm_email as confirm_email_async
from customer.tasks import send_passsword_token
from customer.models import UserChangePassword

import logging

logger = logging.getLogger(__name__)


def create_password_change_token(email):
    token = uuid.uuid4()
    user = User.objects.get(email = email)
    password = None
    try:
        password = UserChangePassword.objects.get(user__id = user.id)
    except UserChangePassword.DoesNotExist:
        password = UserChangePassword(user = user)
    finally:
        password.chpwd_token = token
        password.save()
        send_passsword_token.delay(email, token)
        return token

def confirm_password_token(token, new_password):
    try:
        password = UserChangePassword.objects.get(chpwd_token = token)
        password.delete()
        user = password.user
        user.set_password(new_password)
        user.save()
        return True
    except UserChangePassword.DoesNotExist:
        return False

def create_confirmations(customer):
    # SMS confirmation
    code = str(randint(1000,9999))
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
    print("Sending confirmation sms to ... " + customer.phone)
    confirm_user.delay(customer.phone, code)
    print("Sending email confirmation to " + customer.user.email)
    confirm_email_async.delay(customer.user.email, e_code)
