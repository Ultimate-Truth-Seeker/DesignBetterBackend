from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from apps.usuarios.models import Usuario
from apps.clientes.models import Pedido
from apps.disenadores.models import Diseño
from .forms import AdminUserEditForm, ReporteFilterForm, AsignarPedidoForm, DiseñoAdminForm

# Decorador para verificar si el usuario es administrador
def es_administrador(user):
    return user.is_authenticated and user.rol == 'ADMIN'

# --- Vistas de Usuarios ---
@user_passes_test(es_administrador)
def lista_usuarios(request):
    form = ReporteFilterForm(request.GET or None)
    usuarios = Usuario.objects.all()

    if form.is_valid():
        if form.cleaned_data['rol']:
            usuarios = usuarios.filter(rol=form.cleaned_data['rol'])
        if form.cleaned_data['fecha_inicio']:
            usuarios = usuarios.filter(date_joined__gte=form.cleaned_data['fecha_inicio'])
        if form.cleaned_data['fecha_fin']:
            usuarios = usuarios.filter(date_joined__lte=form.cleaned_data['fecha_fin'])

    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'administracion/usuarios/lista.html', {
        'page_obj': page_obj,
        'form': form
    })

@user_passes_test(es_administrador)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('administracion:lista_usuarios')
    else:
        form = AdminUserEditForm(instance=usuario)
    return render(request, 'administracion/usuarios/editar.html', {'form': form})

# --- Vistas de Pedidos ---
@user_passes_test(es_administrador)
def lista_pedidos(request):
    pedidos = Pedido.objects.select_related('cliente', 'disenador_asignado').all()
    return render(request, 'administracion/pedidos/lista.html', {'pedidos': pedidos})

@user_passes_test(es_administrador)
def asignar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        form = AsignarPedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('administracion:lista_pedidos')
    else:
        form = AsignarPedidoForm(instance=pedido)
    return render(request, 'administracion/pedidos/asignar.html', {'form': form})

# --- Vistas de Diseños ---
@user_passes_test(es_administrador)
def lista_diseños(request):
    diseños = Diseño.objects.all()
    return render(request, 'administracion/disenos/lista.html', {'disenos': diseños})

@user_passes_test(es_administrador)
def editar_diseño(request, diseño_id):
    diseño = get_object_or_404(Diseño, id=diseño_id)
    if request.method == 'POST':
        form = DiseñoAdminForm(request.POST, instance=diseño)
        if form.is_valid():
            form.save()
            return redirect('administracion:lista_diseños')
    else:
        form = DiseñoAdminForm(instance=diseño)
    return render(request, 'administracion/disenos/editar.html', {'form': form})

# --- Dashboard Principal ---
@user_passes_test(es_administrador)
def dashboard(request):
    stats = {
        'total_usuarios': Usuario.objects.count(),
        'total_pedidos': Pedido.objects.count(),
        'pedidos_pendientes': Pedido.objects.filter(estado='PENDIENTE').count(),
    }
    return render(request, 'administracion/dashboard.html', {'stats': stats})