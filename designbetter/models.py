from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, correo_electronico, nombre, password=None, rol='cliente'):
        if not correo_electronico:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(correo_electronico)
        user = self.model(correo_electronico=email, nombre=nombre, rol=rol)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_electronico, nombre, password):
        user = self.create_user(correo_electronico, nombre, password, rol='administrador')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('diseñador', 'Diseñador'),
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
    ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROLES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre']

    objects = UsuarioManager()

    def save(self, *args, **kwargs):
        # Si el rol es administrador, le damos permisos de superusuario
        if self.rol == 'administrador':
            self.is_staff = True
            self.is_superuser = True
            self.is_active = True  # Opcional: activarlo automáticamente
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.correo_electronico
