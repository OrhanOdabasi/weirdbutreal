# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 13:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0031_confirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='confirmed',
            field=models.BooleanField(default=False, verbose_name='Email Confirmerd'),
        ),
        migrations.AlterField(
            model_name='confirmation',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]