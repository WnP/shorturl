# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-18 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortUrl', '0004_auto_20171218_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='url_long',
            field=models.URLField(max_length=600, unique=True),
        ),
    ]
