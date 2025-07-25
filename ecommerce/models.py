from django.db import models
from designbetter.models import *

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
    plantilla = models.ForeignKey(
        PlantillaPrenda,
        on_delete=models.CASCADE,
        related_name='pedidos_personalizados'
    )
    #material = models.ForeignKey(
       # Material,
      #  on_delete=models.CASCADE,
     #   related_name='pedidos_personalizados'
    #)
    color = models.CharField(max_length=50)
    ajustes = models.TextField(blank=True)
    notas = models.TextField(blank=True)
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