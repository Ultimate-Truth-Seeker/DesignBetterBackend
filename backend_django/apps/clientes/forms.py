from django import forms
from .models import Pedido, Feedback

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['titulo', 'descripcion', 'archivo_diseno']  # Campos editables por el cliente
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comentario', 'calificacion']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }