# Generated by Django 2.0.6 on 2019-01-29 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interns', '0008_auto_20190128_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profilePhoto',
            field=models.FileField(null=True, upload_to='images/', verbose_name=''),
        ),
    ]
