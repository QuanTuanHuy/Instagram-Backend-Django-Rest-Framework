# Generated by Django 5.0.4 on 2024-04-29 14:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('post', '0005_alter_like_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_post', to='post.post')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_saved', to='account.profile')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]