# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-26 21:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mhap', '0005_profile_l'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='l',
        ),
    ]
