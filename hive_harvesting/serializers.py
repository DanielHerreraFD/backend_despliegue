from rest_framework import serializers
from hive_harvesting.models import harvesting
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

class InputHarvestingSerializer(serializers.ModelSerializer):
    class Meta:
        model = harvesting
        fields = [
            'harvest_date',
            'honey_production',
            'pollen_production',
            'hive_id',
            'beekeeper'
        ]

class OutputHarvestingSerializer(serializers.ModelSerializer):
    beekeeper = CustomUserSerializer()
    hive_id = BeehiveSerializer()

    class Meta:
        model = harvesting
        fields = [
            'id',
            'harvest_date',
            'honey_production',
            'pollen_production',
            'hive_id',
            'beekeeper'
        ]