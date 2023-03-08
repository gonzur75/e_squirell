# Generated by Django 4.1.7 on 2023-03-03 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energy_prices', '0004_alter_energyprice_valid_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='energyprice',
            name='value_inc_vat',
            field=models.DecimalField(decimal_places=2, help_text='energy price per kwh, with Vat', max_digits=4, verbose_name='Price per kwh'),
        ),
    ]
