# Generated by Django 5.0.4 on 2024-04-27 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_post_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
    ]