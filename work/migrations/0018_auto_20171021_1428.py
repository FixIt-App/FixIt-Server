# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-21 14:28
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0017_transaction_third_party_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='third_party_response',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True),
        ),
    ]
