# Generated by Django 3.1.3 on 2021-01-11 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20210106_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name_for_search',
            field=models.CharField(default='', max_length=60),
        ),
    ]
