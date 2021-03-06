# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-18 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('short_url', '0005_auto_20171218_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='url_long',
            field=models.URLField(unique=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='url_short',
            field=models.URLField(max_length=2000, unique=True),
        ),
    ]
