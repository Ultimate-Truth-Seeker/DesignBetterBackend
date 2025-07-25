from django.urls import path
from .views import CrearPedidoPersonalizadoView, ActualizarEstadoPedidoView, HistorialEstadosPedidoView, ActualizarPagoPedidoView

urlpatterns = [
    path('pedidos/crear/', CrearPedidoPersonalizadoView.as_view(), name='crear-pedido'),
    path('pedidos/<int:pk>/estado/', ActualizarEstadoPedidoView.as_view(), name='actualizar-estado-pedido'),
    path('pedidos/<int:pk>/historial/', HistorialEstadosPedidoView.as_view(), name='historial-pedido'),
    path('pedidos/<int:pk>/pago/',ActualizarPagoPedidoView.as_view(),name='actualizar-pago-pedido')
]