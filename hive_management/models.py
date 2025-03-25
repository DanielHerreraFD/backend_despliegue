from django.db import models
from weather_conditions.models import WeatherConditions
from users.models import CustomUser

class Beehive(models.Model):
    registration_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=30)
    open_brood_frames = models.IntegerField()
    capped_brood_frames = models.IntegerField()
    queen_presence = models.BooleanField()
    queen_color = models.CharField(max_length=15)
    origin = models.CharField(max_length=20)
    food_frames = models.IntegerField()
    observations = models.TextField()
    qr_code = models.TextField(blank=False, null=False) 
    id_weather_conditions = models.ForeignKey(WeatherConditions, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    beekeeper_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   
