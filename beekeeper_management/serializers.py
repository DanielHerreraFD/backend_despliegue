from rest_framework import serializers

class InputUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name= serializers.CharField()
    last_name = serializers.CharField()
    identifications = serializers.CharField()
    password = serializers.CharField(min_length=8)
    email = serializers.EmailField()
    phone = serializers.CharField()
    assignment_date = serializers.DateField()
    birth_date = serializers.DateField()
    state = serializers.ChoiceField(choices=[('Active', 'Activo'), ('Deactivate', 'Desactivo')])
    emergency_contact_name = serializers.CharField(max_length=100)
    emergency_contact_phone = serializers.CharField(max_length=20)
    role = serializers.ChoiceField(choices=[('admin', 'Administrador'), ('beekeeper', 'Apicultor')])

class OutputUserSerializer(InputUserSerializer):
    password = None
    accessToken = serializers.CharField(source="access_token")
    refreshToken = serializers.CharField(source="refresh_token")


class InpuEditUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    first_name= serializers.CharField()
    last_name = serializers.CharField()
    identifications = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    assignment_date = serializers.DateField()
    birth_date = serializers.DateField()
    state = serializers.ChoiceField(choices=[('Active', 'Activo'), ('Deactivate', 'Desactivo')])
    emergency_contact_name = serializers.CharField(max_length=100)
    emergency_contact_phone = serializers.CharField(max_length=20)

class OutPutUserDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    identifications = serializers.CharField()
    first_name= serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    assignment_date = serializers.DateField()
    birth_date = serializers.DateField()
    state = serializers.ChoiceField(choices=[('Active', 'Activo'), ('Deactivate', 'Desactivo')])
    emergency_contact_name = serializers.CharField(max_length=100)
    emergency_contact_phone = serializers.CharField(max_length=20)
    role = serializers.ChoiceField(choices=[('admin', 'Administrador'), ('beekeeper', 'Apicultor')])

class EditUserStateSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=[('Active', 'Activo'), ('Deactivate', 'Desactivo')])
