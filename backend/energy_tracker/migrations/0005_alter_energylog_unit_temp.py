# Generated by Django 5.2 on 2025-04-23 12:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energy_tracker', '0004_energylog_device_status_energylog_power_factor_a_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='energylog',
            name='unit_temp',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(-100), django.core.validators.MaxValueValidator(800)]),
        ),
    ]
