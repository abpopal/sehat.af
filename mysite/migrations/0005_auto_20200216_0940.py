# Generated by Django 2.2.7 on 2020-02-16 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_auto_20200126_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blood_records',
            name='bg_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.Blood_Group'),
        ),
    ]
