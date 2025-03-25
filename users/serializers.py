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

class LoginInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)
    
    
class LoginOutputSerializer(serializers.Serializer):
    username = serializers.CharField()
    accessToken = serializers.CharField(source="access_token")
    refreshToken = serializers.CharField(source="refresh_token")
    role= serializers.CharField()
    id_User = serializers.IntegerField()
    state= serializers.ChoiceField(choices=[('Active', 'Activo'), ('Deactivate', 'Desactivo')])

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True) 
