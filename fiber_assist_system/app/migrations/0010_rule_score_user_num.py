# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-24 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rule_score_rule_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule_score',
            name='user_num',
            field=models.IntegerField(default=0, verbose_name='打分人数'),
        ),
    ]