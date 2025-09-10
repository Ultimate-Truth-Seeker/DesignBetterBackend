from rest_framework import serializers
from .models import Conversacion, Mensaje
from designbetter.models import Usuario

class UsuarioSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "username", "rol"]

class MensajeSerializer(serializers.ModelSerializer):
    remitente = UsuarioSimpleSerializer(read_only=True)

    class Meta:
        model = Mensaje
        fields = ["id", "remitente", "rol_remitente", "contenido", "enviado_en"]

class ConversacionSerializer(serializers.ModelSerializer):
    participantes = UsuarioSimpleSerializer(many=True, read_only=True)
    mensajes = MensajeSerializer(many=True, read_only=True)

    class Meta:
        model = Conversacion
        fields = ["id", "participantes", "mensajes", "creado_en"]
