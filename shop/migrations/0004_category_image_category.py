# Generated by Django 4.2.1 on 2024-01-26 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_category',
            field=models.ImageField(null=True, upload_to='category_images/'),
        ),
    ]
