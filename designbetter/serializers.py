from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dj_rest_auth.serializers import JWTSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario, DxfFile, PatronBase, PartePatron, Material, PlantillaMaterial, PlantillaPrenda
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