# Generated by Django 4.0.4 on 2022-06-04 20:31

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_posts_alter_profile_avatar_alter_profile_cover'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='posts')),
                ('caption', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2022, 6, 4, 21, 31, 1, 869487))),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='Posts',
        ),
    ]