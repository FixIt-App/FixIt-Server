# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-21 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0018_auto_20171021_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='state',
            field=models.CharField(choices=[('CREATING', 'CREATING'), ('CHARGE', 'CHARGE'), ('ROLLBACKED', 'ROLLBACKED'), ('PAYED', 'PAYED')], default='CREATING', max_length=20),
        ),
    ]
