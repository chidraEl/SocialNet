# Generated by Django 4.0.4 on 2022-06-04 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_profile_cover_alter_profile_avatart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='avatart',
            new_name='avatar',
        ),
    ]
