# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-30 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0005_auto_20170506_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('WC', 'WORK CREATED'), ('WA', 'WORKER ASSIGNED'), ('WF', 'WORK FINISHED'), ('PR', 'PROMOTIONAL')], max_length=20),
        ),
    ]