# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-14 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interns', '0018_profile_acceptedinternships'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profilePhoto',
            field=models.FileField(null=True, upload_to='CV/', verbose_name=''),
        ),
    ]
