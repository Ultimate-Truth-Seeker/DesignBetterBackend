from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dj_rest_auth.serializers import JWTSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario
Usuario = get_user_model()

# --- Serializadores existentes (mantén estos) ---
class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ('correo_electronico', 'nombre', 'password', 'rol')

    def create(self, validated_data):
        user = Usuario.objects.create_user(
            correo_electronico=validated_data['correo_electronico'],
            nombre=validated_data['nombre'],
            password=validated_data['password'],
            rol=validated_data.get('rol', 'cliente')
        )
        user.is_active = False
        user.save()
        return user

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.correo_electronico
        token['rol'] = user.rol
        token['nombre'] = user.nombre
        return token
    def validate(self, attrs):
        data = super().validate(attrs)

        # Agregar campos personalizados directamente al nivel superior
        data['email'] = self.user.correo_electronico
        data['rol'] = self.user.rol
        data['nombre'] = self.user.nombre

        return data

class CustomJWTSerializer(JWTSerializer):
    def get_token(self, user):
        token = RefreshToken.for_user(user)
        token['rol'] = user.rol
        token['nombre'] = user.nombre
        token['email'] = user.correo_electronico
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        return data
