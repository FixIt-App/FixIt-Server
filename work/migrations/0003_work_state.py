# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-08 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0002_work_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='state',
            field=models.CharField(choices=[('ORDERED', 'ORDERED'), ('SCHEDULED', 'SCHEDULED'), ('FINISHED', 'FINISHED'), ('FAILED', 'FAILED'), ('CANCELED', 'CANCELED')], default='ORDERED', max_length=20),
        ),
    ]
