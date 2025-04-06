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