# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-24 10:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exam_portal', '0011_studentanswer_marked'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='cnf_password',
            field=models.CharField(default=b'rupanshu', max_length=35),
        ),
        migrations.AddField(
            model_name='student',
            name='password',
            field=models.CharField(default=b'rupanshu', max_length=35),
        ),
    ]