# Generated by Django 4.2.3 on 2023-08-22 20:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance_handler', '0011_alter_balance_balance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='balance_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 22, 20, 32, 3, 758452, tzinfo=datetime.timezone.utc)),
        ),
    ]
