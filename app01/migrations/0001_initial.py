# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-08-10 11:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.IntegerField()),
                ('status', models.IntegerField(choices=[(0, '未支付'), (1, '已支付')], default=0)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Goods')),
            ],
        ),
    ]
