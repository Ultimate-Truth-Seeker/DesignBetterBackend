from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/<int:pedido_id>/feedback/', views.dejar_feedback, name='dejar_feedback'),
]