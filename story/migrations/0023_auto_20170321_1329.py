# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-21 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0022_notification_notify_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='kind',
            field=models.CharField(choices=[('Story', 'Story'), ('CommentLike', 'CommentLike'), ('Comment', 'Comment')], max_length=8),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notifier',
            field=models.CharField(max_length=15),
        ),
    ]