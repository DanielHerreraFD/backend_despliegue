# Generated by Django 5.1.5 on 2025-02-25 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beehive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(max_length=30)),
                ('open_brood_frames', models.IntegerField()),
                ('capped_brood_frames', models.IntegerField()),
                ('queen_presence', models.BooleanField()),
                ('queen_color', models.CharField(max_length=15)),
                ('origin', models.CharField(max_length=20)),
                ('food_frames', models.IntegerField()),
                ('observations', models.CharField(max_length=90)),
                ('qr_code', models.TextField()),
                ('status', models.CharField(max_length=30)),
            ],
        ),
    ]
