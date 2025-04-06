from django.db import models
from apps.usuarios.models import Usuario

class Pedido(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En proceso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    )

    cliente = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'CLIENTE'},
        related_name='pedidos_cliente'
    )
    disenador_asignado = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'rol': 'DISENADOR'},
        related_name='pedidos_disenador'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega_estimada = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    descripcion = models.TextField()
    archivo_diseno = models.FileField(upload_to='pedidos/disenos/', null=True, blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username}"

class Feedback(models.Model):
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    comentario = models.TextField()
    calificacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback para Pedido #{self.pedido.id}"