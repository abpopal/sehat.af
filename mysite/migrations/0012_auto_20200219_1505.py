# Generated by Django 2.2.7 on 2020-02-19 10:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0011_auto_20200219_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='name',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(code='ValueError', message='Name cannot include numbers', regex='^[a-zA-Z ]+$')]),
        ),
        migrations.AlterField(
            model_name='puser',
            name='name',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(code='ValueError', message='Name cannot include numbers', regex='^[a-zA-Z ]+$')]),
        ),
    ]
