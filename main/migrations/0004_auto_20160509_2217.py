# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-09 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20160509_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='code',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
