# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-11-22 12:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20171114_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamer_temp',
            name='applydate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='/media/1.jpg', null=True, upload_to='img'),
        ),
    ]