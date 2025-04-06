from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario  # Importa tu modelo personalizado

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'rol']  # Campos personalizados