# Generated by Django 3.1.3 on 2023-11-22 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0067_auto_20231122_1520'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='location',
            new_name='name',
        ),
    ]
