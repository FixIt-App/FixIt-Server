# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-26 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0019_auto_20170820_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='change_password',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]