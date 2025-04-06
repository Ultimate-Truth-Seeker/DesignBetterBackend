from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pedido, Feedback
from .forms import PedidoForm, FeedbackForm

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user)
    return render(request, 'clientes/pedidos/lista.html', {'pedidos': pedidos})

@login_required
def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = request.user
            pedido.save()
            return redirect('clientes:lista_pedidos')
    else:
        form = PedidoForm()
    return render(request, 'clientes/pedidos/crear.html', {'form': form})

@login_required
def dejar_feedback(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.pedido = pedido
            feedback.save()
            return redirect('clientes:lista_pedidos')
    else:
        form = FeedbackForm()
    return render(request, 'clientes/feedback/crear.html', {'form': form, 'pedido': pedido})