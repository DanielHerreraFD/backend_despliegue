from django.db import models
from users.models import CustomUser
from hive_management.models import Beehive

class Monitoring(models.Model):
    monitoring_date = models.DateTimeField()
    queen_observations = models.TextField()
    food_observations = models.TextField()
    general_observations = models.TextField()
    beekeeper = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hive_id = models.ForeignKey(Beehive, on_delete=models.CASCADE)