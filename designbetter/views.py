from django.shortcuts import render

from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from .serializers import RegistroSerializer
from .utils import generar_token_activacion

class RegistroView(APIView):
    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Crea el usuario (inactivo)

            # Generar token de verificación
            token = generar_token_activacion(user.correo_electronico)

            # Crear la URL de activación
            # Suponiendo que tengas un path como: path('activate/<token>/', ActivarCuentaView.as_view(), ...)
            # O si lo quieres como query param, adaptarlo
            url_activacion = request.build_absolute_uri(
                reverse('activar_cuenta', kwargs={'token': token})
            )

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
    
from django.core.signing import BadSignature
from django.core.signing import Signer

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