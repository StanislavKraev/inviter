# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-09 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='sent_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]