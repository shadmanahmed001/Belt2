# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt_django_app', '0005_auto_20170201_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_user_friends_+', to='belt_django_app.User'),
        ),
    ]