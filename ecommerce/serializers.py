from rest_framework import serializers
from .models import PedidoPersonalizado
from rest_framework import serializers
from .models import PedidoPersonalizado, PedidoEstadoHistoria

class CrearPedidoSerializer(serializers.ModelSerializer):
    # Serializamos el slug del estado
    estado = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug'
    )
    pago_realizado = serializers.BooleanField(read_only=True)
    disenador = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PedidoPersonalizado
        fields = [
            'id',
            'plantilla', 'color', 'ajustes', 'notas', 'usuario', 'disenador',
            'estado', 'pago_realizado',
        ]
        read_only_fields = ['id', 'usuario', 'estado', 'pago_realizado']


class PedidoDetalleSerializer(serializers.ModelSerializer):
    estado = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    pago_realizado = serializers.BooleanField(read_only=True)
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)
    disenador = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PedidoPersonalizado
        fields = [
            'id',
            'plantilla', 'color',
            'ajustes', 'notas',
            'estado', 'pago_realizado',
            'usuario', 'disenador',
            'fecha_creacion',
        ]

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

class PagoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoPersonalizado
        fields = ['pago_realizado']