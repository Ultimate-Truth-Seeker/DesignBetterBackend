from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversacion, Mensaje
from .serializers import ConversacionSerializer, MensajeSerializer
from designbetter.models import Usuario

class ConversacionViewSet(viewsets.ModelViewSet):
    queryset = Conversacion.objects.all()
    serializer_class = ConversacionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_ids = request.data.get("participantes", [])
        if len(user_ids) != 2:
            return Response({"error": "Debes especificar exactamente 2 participantes"}, status=400)

        usuarios = Usuario.objects.filter(id__in=user_ids)
        if usuarios.count() != 2:
            return Response({"error": "Alguno de los usuarios no existe"}, status=400)

        conversacion = Conversacion.objects.create()
        conversacion.participantes.set(usuarios)
        serializer = self.get_serializer(conversacion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        conversacion_id = request.data.get("conversacion")
        contenido = request.data.get("contenido")

        try:
            conversacion = Conversacion.objects.get(id=conversacion_id)
        except Conversacion.DoesNotExist:
            return Response({"error": "Conversación no encontrada"}, status=404)

        mensaje = Mensaje.objects.create(
            conversacion=conversacion,
            remitente=request.user,
            rol_remitente=request.user.rol,
            contenido=contenido
        )

        serializer = self.get_serializer(mensaje)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
