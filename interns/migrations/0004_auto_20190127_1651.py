# Generated by Django 2.0.6 on 2019-01-27 16:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interns', '0003_auto_20190127_1650'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Interns',
            new_name='Intern',
        ),
    ]
