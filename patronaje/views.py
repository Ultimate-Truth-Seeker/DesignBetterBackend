from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import DxfFile, PatronBase, PartePatron, PlantillaPrenda, Material
from .serializers import PatronBaseSerializer, PartePatronSerializer, PlantillaPrendaSerializer
from .utils import convert_dxf_to_svg, generar_svg_para_patron
import json

class DxfFileUploadView(APIView):
    def post(self, request):
        serializer = DxfFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatronBaseViewSet(viewsets.ModelViewSet):
    queryset = PatronBase.objects.all()
    serializer_class = PatronBaseSerializer

def patron_svg_view(request, patron_id):
    try:
        patron = PatronBase.objects.get(id=patron_id)
    except PatronBase.DoesNotExist:
        raise Http404("Patrón no encontrado")

    if patron.archivo_patron.endswith(".dxf"):
        svg_string = convert_dxf_to_svg(patron.archivo_patron)
    else:
        svg_string = generar_svg_para_patron(patron_id)
    return HttpResponse(svg_string, content_type="image/svg+xml")

class ListarPatronesView(generics.ListAPIView):
    serializer_class = PatronBaseSerializer
    permission_classes = [IsAuthenticated]

class PlantillaPrendaViewSet(viewsets.ModelViewSet):
    queryset = PlantillaPrenda.objects.all().prefetch_related('materiales', 'patron_base__partes')
    serializer_class = PlantillaPrendaSerializer