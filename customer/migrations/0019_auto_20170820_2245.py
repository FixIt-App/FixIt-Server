# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-20 22:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0018_tpagacustomer_credit_card_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tpagacustomer',
            name='credit_card_id',
            field=models.CharField(blank=True, max_length=300, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='tpagacustomer',
            name='token',
            field=models.CharField(blank=True, max_length=300, null=True, unique=True),
        ),
    ]
