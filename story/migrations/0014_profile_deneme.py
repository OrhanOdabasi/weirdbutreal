# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-21 03:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0013_auto_20170220_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='deneme',
            field=models.CharField(blank=True, max_length=160, null=True, verbose_name='deneme'),
        ),
    ]
