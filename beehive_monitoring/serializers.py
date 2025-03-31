from rest_framework import serializers  
from beehive_monitoring.models import Monitoring
from users.models import CustomUser
from hive_management.models import Beehive

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']

class BeehiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beehive
        fields = ['id', 'status']

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
    hive_id = BeehiveSerializer()

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