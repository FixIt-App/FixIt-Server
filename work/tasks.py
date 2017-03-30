# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.decorators import task

@task()
def create_work(work):
    print('creating work started')
    for n in range(0,1000000):
        pass
    print("Finished work")

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
