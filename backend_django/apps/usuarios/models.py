from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):  # Extiende el modelo User por defecto de Django
    ROLES = (
        ('CLIENTE', 'Cliente'),
        ('DISENADOR', 'Diseñador'),
        ('ADMIN', 'Administrador'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='CLIENTE')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"