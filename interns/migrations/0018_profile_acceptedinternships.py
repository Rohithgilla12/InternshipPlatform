# Generated by Django 2.0.6 on 2019-02-11 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interns', '0017_profile_enrolledinternships'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='acceptedInternships',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
