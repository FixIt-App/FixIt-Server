from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.decorators import task

import sendgrid
from sendgrid.helpers.mail import *

import os
import boto3



@task()
def confirm_user(phone, code):
    sns = boto3.client('sns')
    print("Text message to " + phone)
    result = sns.publish(
        PhoneNumber = phone,
        Message = 'Bienvenido a FixIt, tu codigo es: %s.' % code,
    )
    print(result)

@task()
def confirm_email(email, code):
    subject = 'Confirma tu correo de FixIt'
    message = "Bienvenido a fixit, puedes entrar en http://%s/confirmations/%s/" % (os.environ.get('DNS_NAME'), code )
    print('Trying to send confirmation email')
    sg = sendgrid.SendGridAPIClient(apikey = os.environ.get('EMAIL_API_KEY'))
    from_email = Email("info@fixitgroup.co")
    to_email = Email(email)
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    



