# Generated by Django 3.1.3 on 2023-10-14 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0042_auto_20231014_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='patient_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
