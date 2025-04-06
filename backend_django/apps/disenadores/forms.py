from django import forms
from .models import Diseño, ProgresoPedido

class DiseñoForm(forms.ModelForm):
    class Meta:
        model = Diseño
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProgresoPedidoForm(forms.ModelForm):
    class Meta:
        model = ProgresoPedido
        fields = ['etapa', 'completado', 'notas']
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }