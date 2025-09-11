from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversacion, Mensaje
from .serializers import ConversacionSerializer, MensajeSerializer
from backend_django.apps.usuarios.models import Usuario

class CrearConversacionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversacionSerializer

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

class ListaConversacionesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversacionSerializer

    def get_queryset(self):
        return Conversacion.objects.filter(participantes=self.request.user)

class DetalleConversacionView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversacionSerializer
    queryset = Conversacion.objects.all()

class EnviarMensajeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MensajeSerializer

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

class ListaMensajesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MensajeSerializer

    def get_queryset(self):
        conversacion_id = self.kwargs['conversacion_id']
        return Mensaje.objects.filter(conversacion_id=conversacion_id)