# accounts/serializers.py

# tu_app/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

Usuario = get_user_model()

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ('correo_electronico', 'nombre', 'password', 'rol')

    def create(self, validated_data):
        # Asignamos is_active=False para requerir confirmación de correo
        user = Usuario.objects.create_user(
            correo_electronico=validated_data['correo_electronico'],
            nombre=validated_data['nombre'],
            password=validated_data['password'],
            rol=validated_data.get('rol', 'cliente')
        )
        user.is_active = False
        user.save()
        return user