# Generated by Django 4.2.3 on 2023-09-08 20:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('balance_handler', '0012_alter_balance_balance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='balance_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
