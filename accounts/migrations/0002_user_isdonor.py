# Generated by Django 2.2.7 on 2020-01-26 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isdonor',
            field=models.BooleanField(default=False),
        ),
    ]
