# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-16 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_analysis_manage_is_show'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis_manage',
            name='ana_id',
            field=models.CharField(max_length=100, verbose_name='分析id'),
        ),
        migrations.AlterField(
            model_name='analysis_manage',
            name='ana_name',
            field=models.CharField(max_length=100, verbose_name='分析管理名'),
        ),
    ]
