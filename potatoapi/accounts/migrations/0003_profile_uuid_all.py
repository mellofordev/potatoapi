# Generated by Django 3.2.4 on 2021-09-14 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_ipaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='uuid_all',
            field=models.IntegerField(null=True),
        ),
    ]