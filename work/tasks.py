from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.decorators import task

from django.contrib.auth import get_user_model

import sendgrid
from sendgrid.helpers.mail import *

import os
from work.models import Work

@task()
def create_work(workid):
    print('creating work started... sending email')
    work = Work.objects.filter(id = workid).first()
    
    message = "El usuario "
    message += work.customer.user.username
    message += " ha creado un trabajo con descripción: "
    message += work.description 
    message += " de tipo "
    message += work.worktype.name
    message += ". A trabajar!"

    # get administrative users to send emails
    users = get_user_model().objects.filter(is_superuser =  True)
    for user in users:
        complete_message = "Hola, " + user.first_name + " " + message
        send_email("desarrollo@fixitgroup.co", user.email, "FixIt - Se ha creado un trabajo!", complete_message)
    print("Finished work... email sent")

    
def send_email(from_email, to_email, subject, message):
    sent_to = to_email
    sg = sendgrid.SendGridAPIClient(apikey = os.environ.get('EMAIL_API_KEY'))
    from_email = Email(from_email)
    to_email = Email(to_email)
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print("se envió un correo a " + sent_to)
    print(response.status_code)
    print(response.body)
    

