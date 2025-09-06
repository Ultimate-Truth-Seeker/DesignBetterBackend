from django.db import models
from designbetter.models import Usuario

class PatronBase(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_prenda = models.CharField(max_length=50)
    genero = models.CharField(max_length=20)
    tallas_disponibles = models.JSONField(blank=True, null=True)  # Ej: ["S", "M", "L"]
    observaciones = models.TextField(blank=True)
    archivo_patron = models.CharField(max_length=255, blank=True)  # Ruta a PDF, DXF, etc.
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    #fecha_creacion = models.DateTimeField(auto_now_add=True)

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
 