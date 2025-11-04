from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversacion, Mensaje
from .serializers import ConversacionSerializer, MensajeSerializer
from designbetter.models import Usuario
import mimetypes
from django.http import FileResponse, HttpResponseRedirect, Http404
from django.core.files.storage import default_storage
from .models import Configuration 

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
    


class ConfigurationExport3DView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            cfg = Configuration.objects.get(pk=pk)
        except Configuration.DoesNotExist:
            return Response({"detail": "Configuration no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        ref = (cfg.mesh3d_ref or "").strip()
        if not ref:
            return Response({"detail": "No existe referencia 3D (mesh3d_ref) para esta configuración."},
                            status=status.HTTP_404_NOT_FOUND)

        # 1) Si es una URL absoluta -> redirect directo
        if ref.startswith("http://") or ref.startswith("https://"):
            return HttpResponseRedirect(ref)

        # 2) Intentar obtener URL desde default_storage (ej: django-storages / S3)
        try:
            storage_url = default_storage.url(ref)
            if storage_url and (storage_url.startswith("http://") or storage_url.startswith("https://")):
                return HttpResponseRedirect(storage_url)
        except Exception:
            # Si storage.url no está implementado o falla, seguimos a la siguiente opción
            pass

        # 3) Si el storage tiene el archivo -> servirlo como descarga
        try:
            if default_storage.exists(ref):
                fh = default_storage.open(ref, mode='rb')
                content_type = mimetypes.guess_type(ref)[0] or 'application/octet-stream'
                response = FileResponse(fh, content_type=content_type)
                filename = ref.split('/')[-1]
                # Cambia 'attachment' por 'inline' si quieres permitir previsualización en navegador
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
        except Exception:
            return Response({"detail": "Error accediendo al archivo 3D en el storage."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Si llegamos aquí, no encontramos el recurso
        return Response({"detail": "Referencia 3D no encontrada en el storage."}, status=status.HTTP_404_NOT_FOUND)
