# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-12 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rule_score_user_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis_manage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ana_id', models.CharField(max_length=20, verbose_name='分析id')),
                ('ana_name', models.CharField(max_length=20, verbose_name='分析管理名')),
            ],
            options={
                'verbose_name': '分析管理',
                'verbose_name_plural': '分析管理',
            },
        ),
    ]
