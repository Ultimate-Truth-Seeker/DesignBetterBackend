from rest_framework.views import APIView
from rest_framework.response import Response
from apps.usuarios.models import Usuario
from .serializers import UsuarioAdminSerializer

class UsuarioAdminAPIView(APIView):
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioAdminSerializer(usuarios, many=True)
        return Response(serializer.data)