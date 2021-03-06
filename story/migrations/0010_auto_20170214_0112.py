# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-13 22:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0009_commentlike_storyupvotes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentlike',
            options={'ordering': ['user'], 'verbose_name': 'Comment Like'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['user'], 'verbose_name': 'User Profile Detail'},
        ),
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['created'], 'verbose_name': 'Story', 'verbose_name_plural': 'Stories'},
        ),
        migrations.AlterModelOptions(
            name='storycomment',
            options={'ordering': ['-comment_date'], 'verbose_name': 'Comment'},
        ),
        migrations.AlterModelOptions(
            name='storyupvotes',
            options={'ordering': ['user'], 'verbose_name': 'Story Upvote List'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, default=None, verbose_name='Birthday'),
        ),
    ]
