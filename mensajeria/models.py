from django.db import models
from django.conf import settings

class Conversacion(models.Model):
    participantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversaciones"
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversación {self.id}"


class Mensaje(models.Model):
    conversacion = models.ForeignKey(
        Conversacion,
        on_delete=models.CASCADE,
        related_name="mensajes"
    )
    remitente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mensajes_enviados"
    )
    rol_remitente = models.CharField(max_length=10)
    contenido = models.TextField()
    enviado_en = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.rol_remitente:
            self.rol_remitente = self.remitente.rol
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Mensaje {self.id} - {self.remitente.username}"
