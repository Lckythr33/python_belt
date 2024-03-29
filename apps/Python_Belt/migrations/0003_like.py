# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-24 18:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Python_Belt', '0002_quote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quotes', models.ManyToManyField(related_name='likes', to='Python_Belt.Quote')),
            ],
        ),
    ]
