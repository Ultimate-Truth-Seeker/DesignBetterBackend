from rest_framework import serializers
from .models import PedidoPersonalizado
from rest_framework import serializers
from .models import PedidoPersonalizado, PedidoEstadoHistoria

class CrearPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoPersonalizado
        # omitimos el campo estado porque lo asignamos siempre a 'pendiente'
        fields = ['id', 'plantilla', 'color', 'ajustes', 'notas']
        read_only_fields = ['id']

class ActualizarEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoPersonalizado
        fields = ['estado']  # solo permitimos cambiar el estado

class PedidoEstadoHistoriaSerializer(serializers.ModelSerializer):
    estado = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    usuario = serializers.StringRelatedField()

    class Meta:
        model = PedidoEstadoHistoria
        fields = ['fecha', 'estado', 'usuario', 'notas']