# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-11-13 18:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20171031_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamer_temp',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photo'),
        ),
    ]
