from rest_framework import serializers
from .models import Beehive
from weather_conditions.models import WeatherConditions
from users.models import CustomUser

class WeatherConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherConditions
        fields = '__all__'
        id_User = serializers.IntegerField(required=True)  

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']


class BeehiveSerializerInput(serializers.ModelSerializer):
    id_weather_conditions = WeatherConditionsSerializer(write_only=True)
    class Meta:
        model = Beehive
        fields = [
            'location',
            'open_brood_frames',
            'capped_brood_frames',
            'queen_presence',
            'queen_color',
            'origin',
            'food_frames',
            'observations',
            'id_weather_conditions',
            'status',
            'beekeeper_id'
        ]

    def create(self, validated_data):
        weather_data = validated_data.pop('id_weather_conditions')
        id_user = validated_data.pop('beekeeper_id')
        weather_conditions = WeatherConditions.objects.create(**weather_data)

        user = id_user or self.context['request'].user


        validated_data['id_weather_conditions'] = weather_conditions
        validated_data['beekeeper_id'] = user 
        return Beehive.objects.create(**validated_data)

class BeehiveSerializerOutput(serializers.ModelSerializer):
    id_weather_conditions = WeatherConditionsSerializer() 
    beekeeper_id = CustomUserSerializer()

    class Meta:
        model = Beehive
        fields = [
            'id',
            'registration_date',
            'location',
            'open_brood_frames',
            'capped_brood_frames',
            'queen_presence',
            'queen_color',
            'origin',
            'food_frames',
            'observations',
            'qr_code',
            'id_weather_conditions',
            'status',
            'beekeeper_id',
        ]
        read_only_fields = fields

class EditBeehiveStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[('Active', 'Activo'), ('Deactivate', 'Desactivo')])