# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-02 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delicontent', '0004_auto_20161224_1255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promoimage',
            options={'verbose_name': 'imagen de promoción', 'verbose_name_plural': 'imágenes de promoción'},
        ),
        migrations.AlterField(
            model_name='page',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='orden para mostrar'),
        ),
        migrations.AlterField(
            model_name='page',
            name='show_in_nav',
            field=models.BooleanField(verbose_name='mostrar en la navegación'),
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(verbose_name='slug'),
        ),
    ]