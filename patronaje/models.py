from django.db import models
from designbetter.models import Usuario

class PatronStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    ARCHIVED = 'archived', 'Archived'

class PatronBase(models.Model):
    code = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="Código único del patrón (p.ej. PAT-TEE-BASIC)"
    )
    name = models.CharField(max_length=150, help_text="Nombre legible del patrón")
    description = models.TextField(blank=True, default="", help_text="Descripción corta")
    category = models.CharField(max_length=100, blank=True, default="", help_text="Categoría / familia")

    status = models.CharField(
        max_length=10,
        choices=PatronStatus.choices,
        default=PatronStatus.DRAFT,
        db_index=True,
        help_text="Estado de publicación"
    )

    params_schema = models.JSONField(
        blank=True, default=dict,
        help_text="JSON Schema de parámetros de entrada"
    )
    constraints = models.JSONField(
        blank=True, default=dict,
        help_text="Reglas/inequations/fórmulas simbólicas"
    )
    pieces = models.JSONField(
        blank=True, default=dict,
        help_text="Definición paramétrica de piezas"
    )
    grading_rules = models.JSONField(
        blank=True, default=dict,
        help_text="Reglas de tallaje/escala"
    )
    geometry_dsl = models.TextField(
        blank=True, null=True,
        help_text="(Opcional) DSL para construir el patrón 2D"
    )

    version = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='patrones_creados'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['code', 'version'],
                name='uq_patron_code_version'
            )
        ]
        indexes = [
            models.Index(fields=['code'], name='idx_patron_code'),
            models.Index(fields=['status'], name='idx_patron_status'),
        ]
        ordering = ['-created_at', '-version']

    def __str__(self):
        code = self.code or "NO-CODE"
        return f"{code} · {self.name} v{self.version}"


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
 