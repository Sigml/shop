# Generated by Django 5.0.1 on 2024-02-11 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_deliveryinfo_house_number_deliveryinfo_street_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryinfo',
            name='apartment_number',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
