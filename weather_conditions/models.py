from django.db import models

class WeatherConditions(models.Model):
    temp_c = models.CharField(max_length=10)
    temp_f = models.CharField(max_length=10)
    text = models.TextField()
    wind_kph = models.CharField(max_length=10)
    pressure_mb = models.CharField(max_length=10,) 
    humidity_indices = models.CharField(max_length=10)
