# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-22 00:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0023_auto_20170321_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='kind',
            field=models.CharField(choices=[('Story', 'Story'), ('CommentLike', 'CommentLike'), ('Comment', 'Comment')], max_length=15),
        ),
    ]
