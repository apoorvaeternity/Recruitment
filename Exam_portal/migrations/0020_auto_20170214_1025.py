# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-14 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exam_portal', '0019_auto_20160922_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='PythonRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('student_number', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
