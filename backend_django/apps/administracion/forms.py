from django import forms
from django.core.exceptions import ValidationError
from apps.usuarios.models import Usuario
from apps.clientes.models import Pedido
from apps.disenadores.models import Diseño

# 1. Formulario para editar usuarios (roles, estado, etc.)
class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'is_active', 'telefono']
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'is_active': 'Cuenta activa',
            'rol': 'Tipo de usuario'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError("Este email ya está registrado.")
        return email

# 2. Formulario para filtrar reportes
class ReporteFilterForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label='Desde'
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label='Hasta'
    )
    rol = forms.ChoiceField(
        choices=[('', 'Todos')] + Usuario.ROLES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        label='Filtrar por rol'
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('fecha_inicio') and cleaned_data.get('fecha_fin'):
            if cleaned_data['fecha_inicio'] > cleaned_data['fecha_fin']:
                raise ValidationError("La fecha de inicio no puede ser mayor a la fecha final.")

# 3. Formulario para asignar pedidos a diseñadores
class AsignarPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['disenador_asignado', 'estado']
        widgets = {
            'disenador_asignado': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

# 4. Formulario para gestionar diseños
class DiseñoAdminForm(forms.ModelForm):
    class Meta:
        model = Diseño
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'disponible']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }