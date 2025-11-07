from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    pass

class Cliente(models.Model):
    usuario = models.OneToOneField('clientes.Usuario', on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=20, blank=True, null=True)
    numero_documento = models.CharField(max_length=50, blank=True, null=True)
    puntos = models.IntegerField(default=0)
    estado = models.CharField(max_length=20, default='ACTIVO')
