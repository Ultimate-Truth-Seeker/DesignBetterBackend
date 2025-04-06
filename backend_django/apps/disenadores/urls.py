from django.urls import path
from . import views

app_name = 'disenadores'

urlpatterns = [
    path('pedidos/', views.lista_pedidos_asignados, name='lista_pedidos'),
    path('pedidos/<int:pedido_id>/progreso/', views.actualizar_progreso, name='actualizar_progreso'),
    path('disenos/', views.lista_disenos, name='lista_disenos'),
]