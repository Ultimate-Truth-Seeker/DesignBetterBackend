from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PedidoPersonalizado, EstadoPedido, PedidoEstadoHistoria
from .serializers import CrearPedidoSerializer, ActualizarEstadoSerializer, PedidoEstadoHistoriaSerializer

class CrearPedidoPersonalizadoView(generics.CreateAPIView):
    queryset = PedidoPersonalizado.objects.all()
    serializer_class = CrearPedidoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        estado_inicial = EstadoPedido.objects.get(slug='pendiente')
        serializer.save(
            usuario=self.request.user,
            estado=estado_inicial
        )

class ActualizarEstadoPedidoView(generics.UpdateAPIView):
    queryset = PedidoPersonalizado.objects.all()
    serializer_class = ActualizarEstadoSerializer
    permission_classes = [IsAuthenticated]
    def perform_update(self, serializer):
        pedido = self.get_object()
        nuevo_estado = serializer.validated_data['estado']
        usuario = self.request.user

        # Guardamos el nuevo estado en el pedido
        serializer.save()

        # Creamos la entrada en el historial
        PedidoEstadoHistoria.objects.create(
            pedido=pedido,
            estado=nuevo_estado,
            usuario=usuario,
            # puedes pasar notas si lo deseas; aquí lo dejamos vacío
        )

class HistorialEstadosPedidoView(generics.ListAPIView):
    serializer_class = PedidoEstadoHistoriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pedido_id = self.kwargs['pk']
        return PedidoEstadoHistoria.objects.filter(pedido__id=pedido_id)