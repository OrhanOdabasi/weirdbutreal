# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-20 15:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0002_auto_20170120_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='author',
        ),
    ]
