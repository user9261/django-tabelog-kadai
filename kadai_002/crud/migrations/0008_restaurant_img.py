# Generated by Django 5.0.4 on 2024-04-13 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0007_restaurant_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='img',
            field=models.ImageField(blank=True, default='noImage.png', upload_to=''),
        ),
    ]
