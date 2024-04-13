# Generated by Django 5.0.4 on 2024-04-13 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0008_restaurant_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='address',
            field=models.CharField(default='愛知県', max_length=200),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='business_hours',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='phone_number',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='zip_code',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
