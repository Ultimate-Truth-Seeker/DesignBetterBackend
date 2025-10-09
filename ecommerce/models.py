from django.db import models
from designbetter.models import *
from patronaje.models import PlantillaPrenda, Configuration

class EstadoPedido(models.Model):
    """
    Modelo que define los posibles estados de un pedido.
    """
    slug = models.SlugField(
        max_length=20,
        unique=True,
        help_text="Identificador interno (p.ej. 'pendiente', 'diseño', ...)."
    )
    nombre = models.CharField(
        max_length=50,
        help_text="Nombre legible del estado (p.ej. 'Pendiente', 'En Diseño', ...)."
    )
    orden = models.PositiveSmallIntegerField(
        help_text="Orden en que se presentan los estados (para listas y UI)."
    )
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción opcional del estado."
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['orden']
        verbose_name = "Estado de Pedido"
        verbose_name_plural = "Estados de Pedido"

    def __str__(self):
        return self.nombre

class PedidoPersonalizado(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('diseño', 'Diseño'),
        ('produccion', 'Producción'),
        ('entrega', 'Entrega'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='pedidos_personalizados'
    )
    disenador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidos_como_disenador',
        help_text="Diseñador asignado al pedido"
    )
    configuration = models.ForeignKey(
        Configuration,
        on_delete=models.PROTECT,
        related_name='pedidos'
    )
    estado = models.ForeignKey(
        'ecommerce.EstadoPedido',
        on_delete=models.PROTECT,
        related_name='pedidos',
        help_text="Estado actual del pedido",
        null=True,
    )
    pago_realizado = models.BooleanField(
        default=False,
        help_text="True si el pago ya se efectuó, False en caso contrario"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

from django.conf import settings
from django.db import models

class PedidoEstadoHistoria(models.Model):
    pedido = models.ForeignKey(
        'ecommerce.PedidoPersonalizado',
        on_delete=models.CASCADE,
        related_name='historia_estados'
    )
    estado = models.ForeignKey(
        'ecommerce.EstadoPedido',
        on_delete=models.PROTECT,
        help_text="Estado al que cambió el pedido"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Usuario que hizo el cambio"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(
        blank=True,
        help_text="Notas opcionales sobre el cambio"
    )

    class Meta:
        ordering = ['fecha']
        verbose_name = "Registro de Estado de Pedido"
        verbose_name_plural = "Historial de Estados de Pedido"

    def __str__(self):
        return f"{self.pedido.id} → {self.estado.slug} @ {self.fecha:%Y-%m-%d %H:%M}"


# --- Modelo Review agregado ---
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # templateId: referencia opcional a PlantillaPrenda (ya existe importada arriba)
    plantilla = models.ForeignKey(
        PlantillaPrenda,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        help_text="Referencia opcional a la plantilla (templateId)"
    )

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Calificación numérica (por ejemplo 1-5)"
    )
    title = models.CharField(max_length=255, blank=True, help_text="Título corto de la reseña")
    body = models.TextField(blank=True, help_text="Contenido/descripcion de la reseña")

    reviewer_name = models.CharField(max_length=150, help_text="Nombre del autor de la reseña")
    reviewer_avatar = models.URLField(blank=True, null=True, help_text="URL del avatar del autor")
    reviewer_date = models.DateTimeField(default=timezone.now, help_text="Fecha de la reseña")

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-creado']

    def __str__(self):
        return f"{self.title or 'Reseña'} — {self.rating}/5 por {self.reviewer_name}"

from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _

class PricingRuleScope(models.TextChoices):
    TEMPLATE = 'template', _('Template')
    PATTERN  = 'pattern',  _('Pattern')
    GLOBAL   = 'global',   _('Global')

class PricingRule(models.Model):
    name  = models.CharField(max_length=150)
    scope = models.CharField(max_length=10, choices=PricingRuleScope.choices, db_index=True)

    target_template = models.ForeignKey(
        'patronaje.PlantillaPrenda',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='pricing_rules',
        help_text="Solo si scope='template'"
    )
    target_pattern = models.ForeignKey(
        'patronaje.PatronBase',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='pricing_rules',
        help_text="Solo si scope='pattern'"
    )

    condition = models.JSONField(default=dict, blank=True)
    action    = models.JSONField(default=dict, blank=True)

    priority  = models.IntegerField(default=0, db_index=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to   = models.DateTimeField(null=True, blank=True)
    stop       = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['priority','id']
        indexes  = [
            models.Index(fields=['scope','priority']),
            models.Index(fields=['target_template','priority']),
            models.Index(fields=['target_pattern','priority']),
        ]
        verbose_name = "Regla de Precio"
        verbose_name_plural = "Reglas de Precio"

    def __str__(self):
        base = self.name or f"Regla {self.pk}"
        if self.scope == PricingRuleScope.TEMPLATE and self.target_template_id:
            return f"{base} [template:{self.target_template_id}]"
        if self.scope == PricingRuleScope.PATTERN and self.target_pattern_id:
            return f"{base} [pattern:{self.target_pattern_id}]"
        return f"{base} [global]"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.scope == PricingRuleScope.TEMPLATE:
            if not self.target_template_id:
                raise ValidationError("target_template es obligatorio cuando scope='template'.")
            if self.target_pattern_id:
                raise ValidationError("No mezclar target_template y target_pattern.")
        elif self.scope == PricingRuleScope.PATTERN:
            if not self.target_pattern_id:
                raise ValidationError("target_pattern es obligatorio cuando scope='pattern'.")
            if self.target_template_id:
                raise ValidationError("No mezclar target_template y target_pattern.")
        else:  # global
            if self.target_template_id or self.target_pattern_id:
                raise ValidationError("Global no debe tener target_* asignado.")
