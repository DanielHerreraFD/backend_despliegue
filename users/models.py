from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    identifications = models.CharField(max_length=20, unique=True) 
    phone = models.CharField(max_length=20) 
    assignment_date = models.DateField(default=timezone.now)
    birth_date = models.DateField(default=timezone.now)
    STATE_CHOICES = [
        ('Active','Activo'),
        ('Deactivate', 'Desactivo'),
    ]
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='Active') 
    emergency_contact_name = models.CharField(max_length=100) 
    emergency_contact_phone = models.CharField(max_length=20) 

    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('beekeeper', 'Apicultor'),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='admin')

class Login(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    date_login = models.DateTimeField()
    id_User = models.ForeignKey(CustomUser, on_delete=models.CASCADE)