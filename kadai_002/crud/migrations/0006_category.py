# Generated by Django 5.0.4 on 2024-04-13 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0005_rename_price_restaurant_max_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
