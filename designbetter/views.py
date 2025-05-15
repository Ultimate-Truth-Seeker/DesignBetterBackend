from django.shortcuts import render

from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from .serializers import RegistroSerializer, DxfFileSerializer
from .utils import generar_token_activacion

from django.conf import settings


from django.core.signing import BadSignature
from django.core.signing import Signer

class RegistroView(APIView):
    def post(self, request):
        signer = Signer()
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Crea el usuario (inactivo)

            # Generar token de verificación
            token = generar_token_activacion(user.correo_electronico)

            # Crear la URL de activación
            # Suponiendo que tengas un path como: path('activate/<token>/', ActivarCuentaView.as_view(), ...)
            # O si lo quieres como query param, adaptarlo
            #url_activacion = request.build_absolute_uri(
            #    reverse('activar_cuenta', kwargs={'token': token})
            #)
            correo_electronico = signer.unsign(token)

            #ruta_relativa = reverse('activate', kwargs={'token': token})
            url_activacion = f"{settings.FRONTEND_DOMAIN}/activate/{token}/"

            # Enviar el correo de activación
            asunto = 'Activa tu cuenta'
            mensaje = f'Hola {user.nombre}, haz click en el siguiente enlace para activar tu cuenta: {url_activacion}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.correo_electronico]
            send_mail(asunto, mensaje, from_email, recipient_list)

            return Response(
                {'detail': 'Usuario creado. Revisa tu correo para activar la cuenta.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ActivarCuentaView(APIView):
    def get(self, request, token):
        signer = Signer()
        try:
            correo_electronico = signer.unsign(token)
            # Buscamos al usuario
            from django.contrib.auth import get_user_model
            Usuario = get_user_model()
            user = Usuario.objects.get(correo_electronico=correo_electronico)
            user.is_active = True
            user.save()
            return Response({'detail': 'Cuenta activada con éxito. Ya puedes iniciar sesión.'})
        except (BadSignature, Usuario.DoesNotExist):
            return Response({'detail': 'Token inválido o usuario no existe.'},
                            status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('correo_electronico')
        if not email:
            return Response({'error': 'Falta el correo_electronico'}, status=400)
        
        try:
            user = User.objects.get(correo_electronico=email)
        except User.DoesNotExist:
            return Response({'message': 'Si el correo existe, se enviará un enlace de reseteo.'}, status=200)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"  # FRONTEND URL

        send_mail(
            subject="Reseteo de contraseña",
            message=f"Usa este link para resetear tu contraseña: {reset_link}",
            from_email="no-reply@tusitio.com",
            recipient_list=[email],
        )

        return Response({'message': 'Se ha enviado un correo si el usuario existe.'}, status=200)

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers

class PasswordResetConfirmView(APIView):
    class InputSerializer(serializers.Serializer):
        uid = serializers.CharField()
        token = serializers.CharField()
        nueva_contraseña = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        nueva_contraseña = serializer.validated_data['nueva_contraseña']

        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({'error': 'Enlace inválido'}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Token inválido o expirado'}, status=400)

        user.set_password(nueva_contraseña)
        user.save()
        return Response({'message': 'Contraseña actualizada con éxito'})
    
# myapp/views.py
from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

User = get_user_model()

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token_str = request.data.get('refresh')
        if not refresh_token_str:
            return Response({'error': 'No se proporcionó refresh token'}, status=400)

        try:
            refresh = RefreshToken(refresh_token_str)
            user = User.objects.get(id=refresh['user_id'])
        except Exception as e:
            return Response({'error': str(e)}, status=401)

        new_access_token = CustomTokenObtainPairSerializer.get_token(user).access_token

        return Response({
            'access': str(new_access_token),
            'refresh': str(refresh_token_str),
            'email': user.correo_electronico,
            'rol': user.rol,
            'nombre': user.nombre,
        })

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        data = self.request.data.copy()

        # Si viene como "access_token", lo mapeamos como id_token
        if "access_token" in data and "id_token" not in data:
            data["id_token"] = data["access_token"]

        kwargs['data'] = data
        return serializer_class(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.user
        if not user.is_active:
            user.is_active = True
            user.save()
        # Generar tokens JWT manualmente
        refresh = RefreshToken.for_user(user)
        refresh['rol'] = user.rol
        refresh['nombre'] = user.nombre
        refresh['email'] = user.correo_electronico

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'email': user.correo_electronico,
                'nombre': user.nombre,
                'rol': user.rol,
            }
        })

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class AsignarRolView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        usuario = request.user
        nuevo_rol = request.data.get("rol")

        # Verificamos si ya tiene un rol
        if usuario.rol:
            return Response({"error": "El rol ya ha sido asignado."}, status=status.HTTP_400_BAD_REQUEST)

        if not nuevo_rol:
            return Response({"error": "Debes proporcionar un rol."}, status=status.HTTP_400_BAD_REQUEST)

        # Validación del rol (si usas choices o tabla de roles)
        ROLES_VALIDOS = ["cliente", "diseñador"]
        if nuevo_rol not in ROLES_VALIDOS:
            return Response({"error": "Rol inválido."}, status=status.HTTP_400_BAD_REQUEST)

        # Asignamos el rol
        usuario.rol = nuevo_rol
        usuario.save()

        return Response({"mensaje": f"Rol '{nuevo_rol}' asignado correctamente."}, status=status.HTTP_200_OK)
    
from .models import DxfFile

class DxfFileUploadView(APIView):
    def post(self, request):
        serializer = DxfFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .models import PatronBase, PartePatron
from .serializers import PatronBaseSerializer, PartePatronSerializer

class PatronBaseViewSet(viewsets.ModelViewSet):
    queryset = PatronBase.objects.all()
    serializer_class = PatronBaseSerializer

class PartePatronViewSet(viewsets.ModelViewSet):
    queryset = PartePatron.objects.all()
    serializer_class = PartePatronSerializer

from django.http import HttpResponse, Http404
from .utils import convert_dxf_to_svg, generar_svg_para_patron
def patron_svg_view(request, patron_id):
    try:
        patron = PatronBase.objects.get(id=patron_id)
    except PatronBase.DoesNotExist:
        raise Http404("Patrón no encontrado")

    if patron.archivo_patron.endswith(".dxf"):
        svg_string = convert_dxf_to_svg(patron.archivo_patron)
    else:
        svg_string = generar_svg_para_patron(patron_id)
    return HttpResponse(svg_string, content_type="image/svg+xml")

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PatronBase, Material
from .serializers import PatronBaseSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class CrearPatronView(generics.CreateAPIView):
    """
    Vista para crear patrones con partes anidadas y materiales.
    Requiere autenticación JWT.
    """
    queryset = PatronBase.objects.all()
    serializer_class = PatronBaseSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Para manejar archivos

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario logeado como creador
        serializer.save(creado_por=self.request.user)

class ListarPatronesView(generics.ListAPIView):
    """
    Vista para listar patrones con filtros básicos.
    """
    serializer_class = PatronBaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = PatronBase.objects.all()
        
        # Filtros opcionales (ej: /api/patrones/?tipo_prenda=camisa)
        tipo_prenda = self.request.query_params.get('tipo_prenda')
        if tipo_prenda:
            queryset = queryset.filter(tipo_prenda=tipo_prenda)
            
        return queryset
from .models import PlantillaPrenda
from .serializers import PlantillaPrendaSerializer

class PlantillaPrendaViewSet(viewsets.ModelViewSet):
    queryset = PlantillaPrenda.objects.all().prefetch_related('materiales', 'patron_base__partes')
    serializer_class = PlantillaPrendaSerializer