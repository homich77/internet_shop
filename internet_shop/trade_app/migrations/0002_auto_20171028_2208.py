# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-28 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='min_price',
            field=models.PositiveIntegerField(),
        ),
    ]