# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 05:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='服务器操作系统', max_length=40, verbose_name='课程标签'),
        ),
    ]