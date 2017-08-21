from sendgrid.helpers.mail import *
import sendgrid
import os

from work.models import Work
from work.tasks import send_email_async as send_email

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(pre_save, sender=Work)
def save_profile(sender, instance, **kwargs):
    try:
        previous = Work.objects.get(pk = instance.id)
        validate_work_was_canceled(previous, instance)
        validate_work_has_finished(previous, instance)
    except Work.DoesNotExist:
        pass

def validate_work_was_canceled(previous, current):
    if previous.state != current.state and current.state == 'CANCELED':
        print('El usuario ha cancelado un trabajo')
        message = 'Un usuario ha cancelado el trabajo con id ' + str(current.id)
        users = get_user_model().objects.filter(is_superuser =  True)
        for user in users:
            complete_message = "Hola, " + user.first_name + " " + message
            send_email.delay("desarrollo@fixitgroup.co", user.email, "FixIt - Se ha cancelado un trabajo :(" , complete_message)
    
def validate_work_has_finished(previous, current):
    if previous.state != current.state and current.state == 'FINISHED':
        print('El usuario ha terminado su trabajo exitosamente, ahora hay que integrar el pago')
        print('El usuario ha terminado exitosamente un trabajo')
        message = 'Un usuario ha terminado el trabajo con id ' + str(current.id)
        users = get_user_model().objects.filter(is_superuser =  True)
        for user in users:
            complete_message = "Hola, " + user.first_name + " " + message
            send_email.delay("desarrollo@fixitgroup.co", user.email, "FixIt - Trabajo terminado exitosamente :)" , complete_message)

