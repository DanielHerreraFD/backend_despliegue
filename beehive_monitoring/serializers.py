from rest_framework import serializers  
from beehive_monitoring.models import Monitoring
from users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']


class MonitoringSerializerInput(serializers.ModelSerializer):
    class Meta:
        model = Monitoring
        fields = [
            'monitoring_date',
            'queen_observations', 
            'food_observations', 
            'general_observations', 
            'beekeeper', 
            'hive_id'
        ]

class MonitoringSerializerOutput(serializers.ModelSerializer):
    beekeeper = CustomUserSerializer()

    class Meta:
        model = Monitoring
        fields = [
            'id',
            'monitoring_date', 
            'queen_observations', 
            'food_observations', 
            'general_observations', 
            'beekeeper', 
            'hive_id'
        ]