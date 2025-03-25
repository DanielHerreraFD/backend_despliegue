# Generated by Django 5.1.5 on 2025-02-25 21:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hive_harvesting', '0001_initial'),
        ('hive_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='harvesting',
            name='beekeeper',
            field=models.ForeignKey(limit_choices_to={'role': 'beekeeper'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='harvesting',
            name='hive_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hive_management.beehive'),
        ),
    ]
