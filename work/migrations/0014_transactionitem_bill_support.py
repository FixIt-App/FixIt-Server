# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-15 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0013_transaction_transactionitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionitem',
            name='bill_support',
            field=models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]
