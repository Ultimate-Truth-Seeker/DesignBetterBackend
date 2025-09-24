from rest_framework import serializers
from .models import Review, PedidoPersonalizado, PedidoEstadoHistoria

class CrearPedidoSerializer(serializers.ModelSerializer):
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

class PedidoTrackingSerializer(PedidoDetalleSerializer):
    historial = PedidoEstadoHistoriaSerializer(
        source='pedidoestadohistoria_set',
        many=True,
        read_only=True
    )

    class Meta(PedidoDetalleSerializer.Meta):
        fields = PedidoDetalleSerializer.Meta.fields + ['historial']

class ReviewSerializer(serializers.ModelSerializer):
    templateId = serializers.SerializerMethodField()
    reviewer = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ["id", "templateId", "rating", "title", "body", "reviewer"]

    def get_templateId(self, obj):
        return getattr(obj, "plantilla_id", None)

    def get_reviewer(self, obj):
        user = getattr(obj, "usuario", None)
        if user is not None:
            display_name = getattr(user, "get_full_name", lambda: "")() or getattr(user, "username", "Cliente")
        else:
            display_name = getattr(obj, "reviewer_name", None) or "Cliente"

        dt = (
            getattr(obj, "created_at", None)
            or getattr(obj, "creado", None)
            or getattr(obj, "created", None)
            or getattr(obj, "reviewer_date", None)
        )
        date_iso = dt.isoformat() if dt else None

        return {
            "name": display_name,
            "avatar": getattr(obj, "reviewer_avatar", None),
            "date": date_iso,
        }

class CreateReviewSerializer(serializers.Serializer):
    templateId = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    title = serializers.CharField(allow_blank=True, required=False)
    body = serializers.CharField(allow_blank=True, required=False)

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        template_id = attrs.get("templateId")

        has_order = PedidoPersonalizado.objects.filter(
            usuario=user,
            plantilla_id=template_id,
            pago_realizado=True,
        ).exists()
        if not has_order:
            raise serializers.ValidationError("Solo puedes reseñar plantillas que hayas comprado.")

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        review = Review.objects.create(
            plantilla_id=validated_data["templateId"],
            usuario=user,
            rating=validated_data["rating"],
            title=validated_data.get("title", ""),
            body=validated_data.get("body", ""),
        )
        return review