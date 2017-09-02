from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.decorators import task

import sendgrid
from sendgrid.helpers.mail import *

import os
import boto3

from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context

from util.mail import send_fixit_email


@task()
def confirm_user(phone, code):
    sns = boto3.client('sns')
    print("Text message to " + phone)
    result = sns.publish(
        PhoneNumber = phone,
        Message = 'Bienvenido a FixIt, tu codigo es: %s' % code,
    )
    print(result)

@task()
def confirm_email(email, code):
    print('Trying to send confirmation email')
    print('hola hola')
    template =  get_template('emails/confirmation.html')
    url = 'http://%s/confirmations/%s/' % (os.environ.get('DNS_NAME'), code )
    context = {'url': url}
    subject = 'Confirma tu correo de FixIt'
    message = template.render(context)
    sg = sendgrid.SendGridAPIClient(apikey = os.environ.get('EMAIL_API_KEY'))
    from_email = Email("info@fixitgroup.co")
    to_email = Email(email)
    content = Content("text/html", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


@task()
def send_passsword_token(email, token):
    user = User.objects.get(email = email)
    template =  get_template('emails/reset_password.html')
    url = 'http://%s/resetear-contrasena/%s/' % (os.environ.get('DNS_NAME'), token)
    context = {'url': url}
    message = template.render(context)
    send_fixit_email('Recupera tu Contraseña', email, 'text/html', message)
    



