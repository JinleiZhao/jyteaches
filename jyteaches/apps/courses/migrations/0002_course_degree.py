# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 04:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[('cj', '初级'), ('zj', '中级'), ('gj', '高级')], default='cj', max_length=20, verbose_name='课程难度'),
        ),
    ]
