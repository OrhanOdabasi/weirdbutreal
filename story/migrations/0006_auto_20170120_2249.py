# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-20 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0005_auto_20170120_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='popularity',
            field=models.IntegerField(verbose_name='Populerlik'),
        ),
    ]
