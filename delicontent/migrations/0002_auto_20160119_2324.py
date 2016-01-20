# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delicontent', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promoimage',
            options={'verbose_name': 'imágen de promoción', 'verbose_name_plural': 'imágenes de promoción'},
        ),
        migrations.AlterField(
            model_name='promoimage',
            name='height',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='promoimage',
            name='width',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
