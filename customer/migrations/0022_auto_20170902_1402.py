# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-02 14:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0021_auto_20170902_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userchangepassword',
            name='chpwd_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
