# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('deliorders', '0017_auto_20150712_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(verbose_name='fecha de entrega', default=datetime.date(2015, 7, 19)),
            preserve_default=True,
        ),
    ]
