from rest_framework import serializers
from ..models import Diseño

class DiseñoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diseño
        fields = ['id', 'nombre', 'categoria', 'precio', 'disponible']