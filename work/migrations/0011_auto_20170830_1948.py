# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-30 19:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0010_auto_20170506_2122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='work',
            name='rating',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='work.Rating'),
        ),
    ]
