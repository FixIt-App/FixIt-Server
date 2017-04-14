# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-13 21:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_customer_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire_date', models.DateTimeField()),
                ('code', models.CharField(max_length=255)),
                ('state', models.BooleanField(default=False)),
                ('confirmation_type', models.CharField(choices=[('MAIL', 'MAIL'), ('SMS', 'SMS')], default='ORDERED', max_length=40)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='confirmations', to='customer.Customer')),
            ],
        ),
    ]
