# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-24 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliproducts', '0027_auto_20160120_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.PositiveIntegerField(null=True, verbose_name='orden'),
        ),
    ]
