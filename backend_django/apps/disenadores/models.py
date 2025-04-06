from django.db import models
from apps.usuarios.models import Usuario

class Diseño(models.Model):
    CATEGORIAS = (
        ('CAMISETA', 'Camiseta'),
        ('VESTIDO', 'Vestido'),
        ('PANTALON', 'Pantalón'),
        ('ACCESORIO', 'Accesorio'),
    )

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    disponible = models.BooleanField(default=True)
    disenador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'DISENADOR'},
        related_name='disenos'
    )
    imagen = models.ImageField(upload_to='disenos/imagenes/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.disenador.username}"

class ProgresoPedido(models.Model):
    pedido = models.ForeignKey(
        'clientes.Pedido',
        on_delete=models.CASCADE,
        related_name='progresos'
    )
    etapa = models.CharField(max_length=50)
    completado = models.BooleanField(default=False)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"Progreso: {self.etapa} (Pedido #{self.pedido.id})"