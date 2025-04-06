from rest_framework import serializers
from apps.usuarios.models import Usuario

class UsuarioAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'is_active']