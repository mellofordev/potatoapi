# Generated by Django 3.2.4 on 2021-08-15 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('pic', models.ImageField(default='default.png', null='True', upload_to='profilepic')),
                ('verified', models.BooleanField(default=False)),
                ('blocked', models.BooleanField(default=False)),
                ('forcelock', models.CharField(choices=[('on', 'ON'), ('off', 'OFF')], default='off', max_length=3)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
