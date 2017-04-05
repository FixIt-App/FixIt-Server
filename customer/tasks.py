from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.decorators import task

import os
import boto3

@task()
def confirm_user(phone):
    sns = boto3.client('sns')
    result = sns.publish(
        PhoneNumber = phone,
        Message = 'Bienvenido a FixIt, tu código es 654'
    )
    print(result)





