# Generated by Django 3.1.3 on 2023-11-25 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0069_users_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='sample_collection',
            new_name='sputum',
        ),
        migrations.RemoveField(
            model_name='users',
            name='vitals',
        ),
    ]
