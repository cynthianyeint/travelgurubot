# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-22 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelguruapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='general',
            name='price_detail',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='general',
            name='promotion_one',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='general',
            name='promotion_two',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='general',
            name='price',
            field=models.CharField(max_length=100, null=True),
        ),
    ]