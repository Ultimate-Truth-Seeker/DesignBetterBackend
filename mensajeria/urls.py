from django.urls import path
from .views import (
    CrearConversacionView,
    ListaConversacionesView,
    DetalleConversacionView,
    EnviarMensajeView,
    ListaMensajesView
)

urlpatterns = [
    path('conversaciones/crear/', CrearConversacionView.as_view(), name='crear-conversacion'),
    path('conversaciones/', ListaConversacionesView.as_view(), name='listar-conversaciones'),
    path('conversaciones/<int:pk>/', DetalleConversacionView.as_view(), name='detalle-conversacion'),
    path('mensajes/enviar/', EnviarMensajeView.as_view(), name='enviar-mensaje'),
    path('mensajes/<int:conversacion_id>/', ListaMensajesView.as_view(), name='listar-mensajes'),
]
