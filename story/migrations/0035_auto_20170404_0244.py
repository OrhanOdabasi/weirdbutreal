# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-04 02:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('story', '0034_auto_20170331_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=69, unique=True, verbose_name='Key')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
                'verbose_name': 'Password Reset Key',
            },
        ),
        migrations.AlterModelOptions(
            name='vote',
            options={'verbose_name': 'Vote'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='confirmed',
            field=models.BooleanField(default=False, verbose_name='Email Confirmed'),
        ),
    ]
