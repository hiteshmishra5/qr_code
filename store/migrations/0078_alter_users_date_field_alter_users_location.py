# Generated by Django 5.0.1 on 2024-02-05 17:18

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0077_alter_users_date_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='date_field',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='users',
            name='location',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='store.location'),
        ),
    ]
