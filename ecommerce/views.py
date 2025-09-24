from django.shortcuts import render
from rest_framework import permissions, status, generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from .models import Review, PedidoPersonalizado, EstadoPedido, PedidoEstadoHistoria
from .serializers import CrearPedidoSerializer, ActualizarEstadoSerializer, PedidoEstadoHistoriaSerializer, PagoPedidoSerializer, PedidoDetalleSerializer, PedidoTrackingSerializer, ReviewSerializer, CreateReviewSerializer
from .permissions import IsCliente, IsDisenador
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

class CrearPedidoPersonalizadoView(generics.CreateAPIView):
    queryset = PedidoPersonalizado.objects.all()
    serializer_class = CrearPedidoSerializer
    permission_classes = [IsAuthenticated, IsCliente]

    def perform_create(self, serializer):
        estado_inicial = EstadoPedido.objects.get(slug='pendiente')
        serializer.save(
            usuario=self.request.user,
            estado=estado_inicial
        )

class ListaPedidosView(generics.ListAPIView):
    """
    GET /pedidos/  → lista sólo los pedidos donde request.user es cliente o diseñador.
    """
    serializer_class = PedidoDetalleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        return PedidoPersonalizado.objects.filter(
            Q(usuario=u) | Q(disenador=u)
        )

class DetallePedidoView(generics.RetrieveAPIView):
    """
    GET /pedidos/{pk}/  → devuelve detalle sólo si request.user está involucrado.
    """
    serializer_class = PedidoDetalleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        return PedidoPersonalizado.objects.filter(
            Q(usuario=u) | Q(disenador=u)
        )

class ActualizarEstadoPedidoView(generics.UpdateAPIView):
    queryset = PedidoPersonalizado.objects.all()
    serializer_class = ActualizarEstadoSerializer
    permission_classes = [IsAuthenticated, IsDisenador]
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
    """
    GET /pedidos/{pk}/historial/
    → Devuelve el historial de estados solo si request.user es cliente o diseñador del pedido.
    """
    serializer_class = PedidoEstadoHistoriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pedido_id = self.kwargs['pk']
        user = self.request.user

        # 1) Cargamos el pedido o 404 si no existe
        pedido = get_object_or_404(PedidoPersonalizado, id=pedido_id)

        # 2) Comprobamos involucramiento
        if not (pedido.usuario == user or pedido.disenador == user):
            raise PermissionDenied("No estás autorizado para ver este historial.")

        # 3) Devolver solo las entradas asociadas a este pedido
        return PedidoEstadoHistoria.objects.filter(pedido=pedido)

class ActualizarPagoPedidoView(generics.UpdateAPIView):
    queryset = PedidoPersonalizado.objects.all()
    serializer_class = PagoPedidoSerializer
    permission_classes = [IsAuthenticated, IsDisenador]

class PedidoTrackingAPIView(RetrieveAPIView):
    queryset = PedidoPersonalizado.objects.all()
    serializer_class = PedidoTrackingSerializer
    lookup_field = 'id'

class CreateReviewView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        output = ReviewSerializer(review).data
        headers = self.get_success_headers(output)
        return Response(output, status=status.HTTP_201_CREATED, headers=headers)


class TemplateReviewsListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        plantilla_id = self.kwargs.get("plantilla_id")
        return Review.objects.filter(plantilla_id=plantilla_id).order_by("-id")