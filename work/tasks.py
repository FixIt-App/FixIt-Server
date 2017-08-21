from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.decorators import task

from django.contrib.auth import get_user_model

import json

import os

import requests

from sendgrid.helpers.mail import *
import sendgrid


from work.models import Work
from work.converters import convert_work_to_dict as convert_work

from worker.models import Worker

from notification.models import Notification, NotificationToken
from notification.notifications.BaseNotification import BaseNotification
from notification.firebase import Firebase

from image.models import Image

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

@task
def send_email_async(from_email, to_email, subject, message):
    send_email(from_email, to_email, subject, message)


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

@task()
def notity_assignment(workid):
    work = Work.objects.get(pk = workid)
    user = work.customer.user

    images = Image.objects.filter(work__id__exact = work.id).all()
    work.images = images
    # setting the worker to the work
    if work.worker is not None:
        worker = Worker.objects.get(pk = work.worker.id)
        work.worker = worker

    serializer = convert_work(work)
    # get all user tokens
    tokens = NotificationToken.objects.filter(token_type = 'CUSTOMER', user__id = user.id).all()
    for token in tokens:
        notification_body = {
            "work": serializer,
            "title": work.worktype.name,
            "body": "Se ha asigando un trabajador"
        }
        notification = BaseNotification(notification = notification_body, to = token.token, priority = 10, notification_type = 'WA')
        saved_notification = Notification(user = user, payload = notification.export(), notification_type = 'WA')
        saved_notification.save()
        sent = Firebase.send_notification(notification)
        if sent is True:
            saved_notification.state = 'DELIVERED'
            saved_notification.save()
        else:
            saved_notification.state = 'FAILED'
            saved_notification.save()
        
    

