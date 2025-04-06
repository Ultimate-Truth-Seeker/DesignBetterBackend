from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.clientes.models import Pedido
from .models import Diseño, ProgresoPedido
from .forms import DiseñoForm, ProgresoPedidoForm

@login_required
def lista_pedidos_asignados(request):
    pedidos = Pedido.objects.filter(
        disenador_asignado=request.user
    ).select_related('cliente')
    return render(request, 'disenadores/pedidos/asignados.html', {'pedidos': pedidos})

@login_required
def actualizar_progreso(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, disenador_asignado=request.user)
    if request.method == 'POST':
        form = ProgresoPedidoForm(request.POST)
        if form.is_valid():
            progreso = form.save(commit=False)
            progreso.pedido = pedido
            progreso.save()
            return redirect('disenadores:lista_pedidos')
    else:
        form = ProgresoPedidoForm()
    return render(request, 'disenadores/pedidos/progreso.html', {'form': form, 'pedido': pedido})

@login_required
def lista_disenos(request):
    disenos = Diseño.objects.filter(disenador=request.user)
    return render(request, 'disenadores/disenos/lista.html', {'disenos': disenos})