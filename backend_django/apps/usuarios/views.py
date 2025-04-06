from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm 

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect('redireccionar_por_rol')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def redireccionar_por_rol(request):
    if request.user.rol == 'CLIENTE':
        return redirect('clientes:inicio')
    elif request.user.rol == 'DISENADOR':
        return redirect('disenadores:inicio')
    elif request.user.rol == 'ADMIN':
        return redirect('admin:index')  # Usa el admin de Django o tu vista personalizada