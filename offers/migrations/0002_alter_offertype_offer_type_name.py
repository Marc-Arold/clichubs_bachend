# Generated by Django 4.2.3 on 2023-08-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offertype',
            name='offer_type_name',
            field=models.CharField(help_text='The type of offer we provide.', max_length=255, unique=True, verbose_name='Offer Type Name'),
        ),
    ]
