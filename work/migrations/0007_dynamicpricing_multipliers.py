# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0006_dynamicpricing'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamicpricing',
            name='multipliers',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=12),
        ),
    ]
