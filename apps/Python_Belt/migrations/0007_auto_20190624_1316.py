# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-24 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Python_Belt', '0006_quote_likedby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='likedby',
            field=models.IntegerField(default=0),
        ),
    ]