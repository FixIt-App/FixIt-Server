# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.decorators import task

import sendgrid
import os
from sendgrid.helpers.mail import *


@task()
def create_work(work):
    print('creating work started... sending email')
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('EMAIL_API_KEY'))
    from_email = Email("desarrollo@fixitgroup.co")
    to_email = Email("davidcalle9430@gmail.com")
    subject = "Se ha creado un trabajo!"
    content = Content("text/plain", "Un usuario ha creado un trabajo nuevo. Asignarle un trabajador ASAP!")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print("Finished work... email sent")
