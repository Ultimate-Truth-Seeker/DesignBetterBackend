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

class PartePatronViewSet(viewsets.ModelViewSet):
    queryset = PartePatron.objects.all()
    serializer_class = PartePatronSerializer

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

class CrearPatronView(generics.CreateAPIView):
    """
    Vista para crear patrones con partes anidadas y materiales.
    Requiere autenticación JWT.
    """
    queryset = PatronBase.objects.all()
    serializer_class = PatronBaseSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Para manejar archivos

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario logeado como creador
        serializer.save(creado_por=self.request.user)
    def post(self, request, *args, **kwargs):
        raw_data = request.data
        data = {}

        for key in raw_data:
            value = raw_data.get(key)

            if key in ['partes'] and isinstance(value, str):
                try:
                    data[key] = json.loads(value)
                except json.JSONDecodeError:
                    return Response({key: 'Formato JSON inválido'}, status=400)
            else:
                data[key] = value
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    

class ListarPatronesView(generics.ListAPIView):
    """
    Vista para listar patrones con filtros básicos.
    """
    serializer_class = PatronBaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = PatronBase.objects.all()
        
        # Filtros opcionales (ej: /api/patrones/?tipo_prenda=camisa)
        tipo_prenda = self.request.query_params.get('tipo_prenda')
        if tipo_prenda:
            queryset = queryset.filter(tipo_prenda=tipo_prenda)
            
        return queryset

class PlantillaPrendaViewSet(viewsets.ModelViewSet):
    queryset = PlantillaPrenda.objects.all().prefetch_related('materiales', 'patron_base__partes')
    serializer_class = PlantillaPrendaSerializer


