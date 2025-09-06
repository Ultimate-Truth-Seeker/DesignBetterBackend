from rest_framework import serializers
from .models import *

class DxfFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DxfFile
        fields = ['id', 'name', 'file', 'uploaded_at']

# --- Serializadores NUEVOS/Modificados para Patrones ---
import json
class MedidasField(serializers.Field):
    """Campo personalizado para validar medidas en formato JSON"""
    def to_representation(self, value):
        return value
    
    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError("Las medidas deben ser un objeto JSON")
        return data

class PartePatronSerializer(serializers.ModelSerializer):
    medidas = serializers.JSONField()
    geometria = serializers.JSONField()
    class Meta:
        model = PartePatron
        fields = ['nombre_parte', 'medidas', 'observaciones', 'geometria']
class PatronBaseSerializer(serializers.ModelSerializer):
    partes = PartePatronSerializer(many=True, write_only=True)  # ← vuelve a esto
    materiales = serializers.PrimaryKeyRelatedField(
        queryset=Material.objects.all(),
        many=True,
        required=False
    )
    archivo_patron = serializers.FileField(required=True)  # Cambiado de CharField a FileField

    class Meta:
        model = PatronBase
        fields = [
            'id', 'nombre', 'tipo_prenda', 'genero', 
            'tallas_disponibles', 'observaciones', 
            'archivo_patron', 'partes', 'materiales',
            #'creado_por', 'fecha_creacion'
        ]
        read_only_fields = ('creado_por', 'fecha_creacion')
        extra_kwargs = {
            'tallas_disponibles': {'required': True}
        }
    def to_internal_value(self, data):
        # Si partes viene como string, deserialízalo
        for campo in ['partes']:
            if isinstance(data.get(campo), str):
                try:
                    data[campo] = json.loads(data[campo])
                except json.JSONDecodeError:
                    raise serializers.ValidationError({campo: 'Formato JSON inválido'})
        return super().to_internal_value(data)
    
    def create(self, validated_data):
        partes_data = validated_data.pop('partes', [])
        
        patron = PatronBase.objects.create(**validated_data)
        
        for parte_data in partes_data:
            PartePatron.objects.create(patron_base=patron, **parte_data)
        
        return patron

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class PlantillaMaterialSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)

    class Meta:
        model = PlantillaMaterial
        fields = ['material']

class PlantillaPrendaSerializer(serializers.ModelSerializer):
    patron_base = PatronBaseSerializer(read_only=True)
    patron_base_id = serializers.PrimaryKeyRelatedField(
        queryset=PatronBase.objects.all(), source='patron_base', write_only=True, required=False
    )
    materiales = serializers.SerializerMethodField()

    class Meta:
        model = PlantillaPrenda
        fields = [
            'id', 'nombre', 'descripcion', 'tipo_ropa', 'tipo_cuerpo',
            'patron_base', 'patron_base_id', 'materiales'
        ]

    def get_materiales(self, obj):
        materiales = PlantillaMaterial.objects.filter(plantilla=obj)
        return PlantillaMaterialSerializer(materiales, many=True).data

