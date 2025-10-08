from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.fields import ArrayField
from decimal import Decimal
from designbetter.models import Usuario
import hashlib
import json

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

# ---------------------------------------
# Estados reutilizables
# ---------------------------------------
class TemplateStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    ARCHIVED = 'archived', 'Archived'

class ConfigurationState(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    READY = 'ready', 'Ready'            # validada / lista para producir
    APPROVED = 'approved', 'Approved'   # aprobada por cliente/operaciones
    ARCHIVED = 'archived', 'Archived'

class MeasurementSource(models.TextChoices):
    TABLE = 'table', 'Tabla de medidas'
    CUSTOM = 'custom', 'Medidas personalizadas'
    CUSTOMER = 'customer', 'Perfil de cliente'

class MeasurementTable(models.Model):
    """
    Tabla de medidas específicas (por género, sistema de tallas, etc.)
    """
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unisex', 'Unisex'),
    ]

    UNIT_SYSTEM_CHOICES = [
        ('metric', 'Metric (cm)'),
        ('imperial', 'Imperial (in)'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=150,
        help_text="Nombre de la tabla (p.ej. 'Tabla Hombres EU', 'Women's Size Chart')"
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='unisex'
    )
    size_system = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Sistema de tallas (p.ej. EU, US, MX)"
    )
    unit_system = models.CharField(
        max_length=10,
        choices=UNIT_SYSTEM_CHOICES,
        default='metric',
        help_text="Sistema de unidades usado en las medidas"
    )
    measures = models.JSONField(
        blank=True,
        default=dict,
        help_text="Diccionario de medidas base (ej. {'bust': 90, 'waist': 70})"
    )
    owner = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='measurement_tables',
        help_text="Usuario propietario o creador de la tabla"
    )
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'version'],
                name='uq_mt_name_ver'
            )
        ]
        indexes = [
            models.Index(fields=['gender'], name='idx_measurementtable_gender'),
            models.Index(fields=['unit_system'], name='idx_mt_unit'),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} v{self.version} ({self.gender})"

# ---------------------------------------
# TEMPLATE (Plantilla de prenda)
# ---------------------------------------
class PlantillaPrenda(models.Model):
    code = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="Código único de plantilla (p.ej. TEE-OXFORD-SLIM)"
    )
    name = models.CharField(max_length=150, help_text="Nombre de la plantilla")
    description = models.TextField(blank=True, default="", help_text="Descripción corta")
    category = models.CharField(max_length=100, blank=True, default="", help_text="Categoría / familia")

    status = models.CharField(
        max_length=10,
        choices=TemplateStatus.choices,
        default=TemplateStatus.DRAFT,
        db_index=True,
        help_text="Estado de publicación"
    )

    # Patrón paramétrico base que instancian las plantillas
    pattern_base = models.ForeignKey(
        PatronBase,
        on_delete=models.PROTECT,
        related_name='plantillas',
        help_text="Patrón paramétrico del cual deriva esta plantilla"
    )

    # Qué parámetros se exponen y con qué UI/valores por defecto
    default_params = models.JSONField(
        blank=True, default=dict,
        help_text="Valores por defecto de parámetros del patrón"
    )
    exposed_options = models.JSONField(
        blank=True, default=dict,
        help_text="Opciones expuestas a UI (select/radio/boolean/range) con metadatos"
    )
    compatibility_rules = models.JSONField(
        blank=True, default=dict,
        help_text="Reglas de compatibilidad entre opciones (forbid/require/if-then)"
    )

    # Políticas de materiales, tallas/medidas objetivo y medios
    materials_policy = models.JSONField(
        blank=True, default=dict,
        help_text="Materiales/acabados permitidos + consumos base"
    )
    size_range = models.JSONField(
        blank=True, default=dict,
        help_text="Definición de tallas/rango (p.ej. XS-XXL) o medidas objetivo"
    )

    # Media opcional
    hero_url = models.URLField(blank=True, null=True)
    gallery = ArrayField(models.URLField(), blank=True, default=list)

    version = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='plantillas_creadas'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    # Campo para búsquedas de texto completo (opcional)
    search_vector = SearchVectorField(null=True, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['code', 'version'],
                name='uq_template_code_version'
            )
        ]
        indexes = [
            models.Index(fields=['code'], name='idx_template_code'),
            models.Index(fields=['status'], name='idx_template_status'),
            GinIndex(fields=['search_vector'], name='idx_template_searchvec'),
        ]
        ordering = ['-created_at', '-version']

    def __str__(self):
        code = self.code or "NO-CODE"
        return f"{code} · {self.name} v{self.version}"


# ---------------------------------------
# CONFIGURATION (Configuración concreta / Pedido)
# ---------------------------------------
class Configuration(models.Model):
    template = models.ForeignKey(
        PlantillaPrenda,
        on_delete=models.PROTECT,
        related_name='configurations',
        help_text="Plantilla desde la cual se crea esta configuración"
    )
    template_version = models.PositiveIntegerField(
        help_text="Versión de la plantilla en el momento de crear la configuración"
    )
    pattern_version = models.PositiveIntegerField(
        help_text="Versión del patrón base en el momento de crear la configuración"
    )

    customer = models.ForeignKey(
        Usuario,#'Customer',  # ajusta si usas otro modelo o app label, o déjalo null si B2B interno
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='configurations',
        help_text="Cliente asociado (opcional)"
    )

    # Origen de las medidas
    measurement_source = models.CharField(
        max_length=10,
        choices=MeasurementSource.choices,
        default=MeasurementSource.TABLE,
        help_text="Fuente de medidas para resolver el patrón"
    )
    measurement_table = models.ForeignKey(
        MeasurementTable,  # crea este modelo o ajusta a tu naming
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='configurations',
        help_text="Tabla de medidas si measurement_source=table"
    )
    # Perfil de cliente o medidas ad-hoc
    custom_measures = models.JSONField(
        blank=True, default=dict,
        help_text="Medidas personalizadas (si measurement_source=custom)"
    )

    # Selecciones del usuario / resolved params después de validaciones
    selected_options = models.JSONField(
        blank=True, default=dict,
        help_text="Opciones seleccionadas por el usuario (collar, puño, etc.)"
    )
    resolved_params = models.JSONField(
        blank=True, default=dict,
        help_text="Parámetros finales tras validación/derivación (incluye holguras, etc.)"
    )

    # Geometría resultante y referencia 3D
    pieces_2d = models.JSONField(
        blank=True, default=dict,
        help_text="Geometría 2D resuelta (líneas/curvas/notches) lista para exportar"
    )
    mesh3d_ref = models.CharField(
        max_length=255,
        blank=True, default="",
        help_text="Ruta/ID a GLB/OBJ generado para preview 3D"
    )

    # Materiales asignados por pieza y despiece
    material_assignments = models.JSONField(
        blank=True, default=dict,
        help_text="Asignación de materiales por pieza/segmento"
    )

    # Costos y precio
    cost_breakdown = models.JSONField(
        blank=True, default=dict,
        help_text="Detalle de costos (materiales, mano de obra, acabados, overhead)"
    )
    price_total = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00'),
        help_text="Precio final calculado tras aplicar reglas"
    )
    currency = models.CharField(max_length=8, default="USD")

    state = models.CharField(
        max_length=10,
        choices=ConfigurationState.choices,
        default=ConfigurationState.DRAFT,
        db_index=True
    )

    # Huella para cachear/reproducir resultados (params + medidas + opciones)
    config_fingerprint = models.CharField(
        max_length=64,
        db_index=True,
        help_text="SHA-256 de (pattern_version, template_version, selected_options, resolved_params, measures)"
    )

    created_by = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='configurations_created'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['state'], name='idx_configuration_state'),
            models.Index(fields=['created_at'], name='idx_configuration_created_at'),
            models.Index(fields=['config_fingerprint'], name='idx_configuration_fingerprint'),
        ]
        ordering = ['-created_at']

        # Evita duplicados exactos de la misma configuración (misma huella) por plantilla
        constraints = [
            models.UniqueConstraint(
                fields=['template', 'config_fingerprint'],
                name='uq_template_fingerprint'
            )
        ]

    def __str__(self):
        return f"Cfg #{self.id} · {self.template} · {self.state}"

    # ---------- Helpers ----------
    @staticmethod
    def _stable_dumps(payload: dict) -> str:
        """Dump JSON estable para hashing (sin espacios y con sort_keys)."""
        return json.dumps(payload or {}, separators=(',', ':'), sort_keys=True, ensure_ascii=False)

    def compute_fingerprint(self) -> str:
        """Calcula un SHA-256 con los elementos que definen la configuración."""
        basis = {
            "pattern_version": self.pattern_version,
            "template_version": self.template_version,
            "measurement_source": self.measurement_source,
            "measurement_table_id": self.measurement_table_id,
            "custom_measures": self.custom_measures or {},
            "selected_options": self.selected_options or {},
            "resolved_params": self.resolved_params or {},
        }
        raw = self._stable_dumps(basis)
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()

    def save(self, *args, **kwargs):
        # Autollenar versiones de plantilla/patrón si no se definieron explícitamente
        if not self.template_version:
            self.template_version = self.template.version
        if not self.pattern_version:
            self.pattern_version = self.template.pattern_base.version

        # Asegurar fingerprint consistente antes de guardar
        self.config_fingerprint = self.compute_fingerprint()
        super().save(*args, **kwargs)

    # Validaciones ligeras (las fuertes pueden vivir en servicios)
    def clean(self):
        # 1) coherencia fuente de medidas
        if self.measurement_source == MeasurementSource.TABLE and not self.measurement_table_id:
            from django.core.exceptions import ValidationError
            raise ValidationError("measurement_table es requerido cuando measurement_source=table.")
        if self.measurement_source == MeasurementSource.CUSTOM and not self.custom_measures:
            from django.core.exceptions import ValidationError
            raise ValidationError("custom_measures es requerido cuando measurement_source=custom.")

        # 2) moneda/precio
        if self.price_total is not None and self.price_total < 0:
            from django.core.exceptions import ValidationError
            raise ValidationError("price_total no puede ser negativo.")

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


class ExportKind(models.TextChoices):
    PDF = 'pdf', 'PDF'
    DXF = 'dxf', 'DXF'
    SVG = 'svg', 'SVG'
    GLB = 'glb', 'GLB'
    TECHPACK = 'techpack', 'TechPack'


class ExportArtifact(models.Model):
    configuration = models.ForeignKey(
        Configuration,
        on_delete=models.CASCADE,
        related_name='export_artifacts',
        help_text="Configuración desde la cual se generó el artefacto"
    )

    kind = models.CharField(
        max_length=16,
        choices=ExportKind.choices,
        db_index=True,
        help_text="Tipo de artefacto exportado"
    )

    # Campo 'path' como string; si prefieres FileField puedes cambiarlo después.
    path = models.CharField(
        max_length=1024,
        help_text="Ruta o identificador del archivo exportado (p.ej. S3 key, path local)"
    )

    metadata = models.JSONField(
        blank=True,
        default=dict,
        help_text="Metadatos adicionales (JSON)"
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['configuration'], name='idx_expart_cfg'),
            models.Index(fields=['kind'], name='idx_exportartifact_kind'),
            models.Index(fields=['created_at'], name='idx_exportartifact_created_at'),
        ]
        ordering = ['-created_at']
        verbose_name = "Export Artifact"
        verbose_name_plural = "Export Artifacts"

    def __str__(self):
        cfg_id = getattr(self.configuration, 'id', None)
        return f"ExportArtifact ({self.kind}) - cfg:{cfg_id} - {self.path}"

class MeasurementSchema(models.Model):
    """
    Catálogo maestro de medidas disponibles y sus reglas de validación.
    Ejemplo: bust, waist, hip, etc.
    """
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Identificador interno de la medida (ej. 'bust', 'waist')"
    )
    display_name = models.CharField(
        max_length=100,
        help_text="Nombre legible de la medida (ej. 'Busto', 'Cintura')"
    )
    unit = models.CharField(
        max_length=10,
        help_text="Unidad base (cm, in, etc.)"
    )
    min = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Valor mínimo permitido (opcional)"
    )
    max = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Valor máximo permitido (opcional)"
    )
    required = models.BooleanField(
        default=False,
        help_text="Indica si esta medida es obligatoria"
    )
    formula_notes = models.TextField(
        blank=True,
        default="",
        help_text="Notas o fórmulas de derivación para esta medida"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['code'], name='idx_measurementschema_code'),
        ]
        ordering = ['code']

    def __str__(self):
        return f"{self.display_name} ({self.code})"


