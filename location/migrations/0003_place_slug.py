# Generated by Django 5.0.4 on 2024-04-25 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_alter_place_latitude_alter_place_longitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]