# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 02:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt_django_app', '0003_auto_20170201_0202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='name',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='users',
        ),
        migrations.AddField(
            model_name='friend',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='belt_django_app.User'),
        ),
    ]