# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 20:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worktype', '0003_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='publications',
            new_name='worktypes',
        ),
    ]
