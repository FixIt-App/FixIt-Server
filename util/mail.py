import os

import sendgrid
from sendgrid.helpers.mail import *

def send_fixit_email(subject, to_email, content_type, email_content):
    send_mail(subject, "info@fixitgroup.co", to_email, content_type, email_content)

def send_mail(subject, from_email, to_email, content_type, email_content):
    sg = sendgrid.SendGridAPIClient(apikey = os.environ.get('EMAIL_API_KEY'))
    from_email = Email(from_email)
    to_email = Email(to_email)
    content = Content(content_type, email_content)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
