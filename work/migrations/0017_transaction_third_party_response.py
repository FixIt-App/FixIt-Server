# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-21 02:12
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0016_auto_20171015_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='third_party_response',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None, null=True),
        ),
    ]