# Generated by Django 5.0.4 on 2024-05-03 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_hashtag_post_hashtags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.URLField(),
        ),
    ]
