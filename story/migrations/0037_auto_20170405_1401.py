# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-05 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0036_auto_20170405_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='vote',
            field=models.CharField(choices=[('Upvote', 'Upvote'), ('Downvote', 'Downvote')], max_length=10, verbose_name='Vote'),
        ),
    ]
