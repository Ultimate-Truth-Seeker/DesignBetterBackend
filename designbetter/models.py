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
        ('', '')
    ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROLES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo_electronico'
    EMAIL_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre']

    objects = UsuarioManager()

    def save(self, *args, **kwargs):
        # Si el rol es administrador, le damos permisos de superusuario
        if self.is_staff and self.is_superuser:
            self.rol = "administrador"
            self.is_active = True  # Opcional: activarlo automáticamente
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.correo_electronico

class PatronBase(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_prenda = models.CharField(max_length=50)
    genero = models.CharField(max_length=20)
    tallas_disponibles = models.JSONField(blank=True, null=True)  # Ej: ["S", "M", "L"]
    observaciones = models.TextField(blank=True)
    archivo_patron = models.CharField(max_length=255, blank=True)  # Ruta a PDF, DXF, etc.
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.nombre


class PlantillaPrenda(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    tipo_ropa = models.CharField(max_length=50)
    tipo_cuerpo = models.CharField(max_length=50)
    patron_base = models.ForeignKey(PatronBase, on_delete=models.SET_NULL, null=True, blank=True, related_name='plantillas')

    def _str_(self):
        return self.nombre


class Material(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def _str_(self):
        return self.nombre


class PlantillaMaterial(models.Model):
    plantilla = models.ForeignKey(PlantillaPrenda, on_delete=models.CASCADE, related_name='materiales')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='plantillas')

    class Meta:
        unique_together = ('plantilla', 'material')

    def _str_(self):
        return f"{self.plantilla.nombre} - {self.material.nombre}"


class PartePatron(models.Model):
    patron_base = models.ForeignKey(PatronBase, on_delete=models.CASCADE, related_name='partes')
    nombre_parte = models.CharField(max_length=50)  # Ej: "Manga", "Cuello"
    medidas = models.JSONField(blank=True, null=True)  # Ej: {"largo": 60, "ancho": 20}
    geometria = models.JSONField(blank=True, null=True)
    observaciones = models.TextField(blank=True)

    def _str_(self):
        return f"{self.nombre_parte} ({self.patron_base.nombre})"
    
class DxfFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='dxf_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)