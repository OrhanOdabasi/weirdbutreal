# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-05 00:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0035_auto_20170404_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='language',
            field=models.CharField(choices=[('En', 'English')], max_length=10, verbose_name='Language'),
        ),
    ]