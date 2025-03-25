# Generated by Django 5.1.5 on 2025-03-08 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Administrador'), ('beekeeper', 'Apicultor')], default='admin', max_length=15, verbose_name='Rol'),
        ),
    ]
