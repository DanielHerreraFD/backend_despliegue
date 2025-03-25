from django.db import models
from users.models import CustomUser
from hive_management.models import Beehive
from django.utils import timezone

class harvesting(models.Model):
    harvest_date = models.DateField(default=timezone.now)
    honey_production = models.FloatField()
    pollen_production = models.FloatField()
    hive_id = models.ForeignKey(Beehive, on_delete=models.CASCADE)
    beekeeper = models.ForeignKey(CustomUser, on_delete=models.CASCADE)