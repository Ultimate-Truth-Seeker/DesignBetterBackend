from django.urls import path
from .views import CrearPedidoPersonalizadoView, ActualizarEstadoPedidoView, HistorialEstadosPedidoView, ActualizarPagoPedidoView, ListaPedidosView, DetallePedidoView, PedidoTrackingAPIView, CreateReviewView, TemplateReviewsListView

urlpatterns = [
    path('pedidos/crear/', CrearPedidoPersonalizadoView.as_view(), name='crear-pedido'),
    path('pedidos/', ListaPedidosView.as_view(), name='listar-pedidos'),
    path('pedidos/<int:pk>/', DetallePedidoView.as_view(), name='detalle-pedido'),
    path('pedidos/<int:pk>/estado/', ActualizarEstadoPedidoView.as_view(), name='actualizar-estado-pedido'),
    path('pedidos/<int:pk>/historial/', HistorialEstadosPedidoView.as_view(), name='historial-pedido'),
    path('pedidos/<int:pk>/pago/',ActualizarPagoPedidoView.as_view(),name='actualizar-pago-pedido'),
    path('api/pedidos/<int:id>/tracking/',PedidoTrackingAPIView.as_view(),name='pedido-tracking'),
    path("orders/reviews/", CreateReviewView.as_view(), name="crear-review"),
    path("orders/plantillas/<int:plantilla_id>/reviews/", TemplateReviewsListView.as_view(), name="reviews-plantilla")
]