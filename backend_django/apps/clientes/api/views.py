from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Pedido
from .serializers import PedidoSerializer

class PedidosClienteAPIView(APIView):
    def get(self, request):
        pedidos = Pedido.objects.filter(cliente=request.user)
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)