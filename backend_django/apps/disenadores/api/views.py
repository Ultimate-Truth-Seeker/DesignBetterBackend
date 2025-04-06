from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Diseño
from .serializers import DiseñoSerializer

class MisDisenosAPIView(APIView):
    def get(self, request):
        disenos = Diseño.objects.filter(disenador=request.user)
        serializer = DiseñoSerializer(disenos, many=True)
        return Response(serializer.data)