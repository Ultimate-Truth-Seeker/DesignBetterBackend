from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'patrones', PatronBaseViewSet, basename='patrones')  # Añadido basename
router.register(r'plantillas', PlantillaPrendaViewSet)

urlpatterns = [
    path('upload-dxf/', DxfFileUploadView.as_view(), name='upload-dxf'),
    
    # API adicional para patrones (filtros personalizados)
    path('patrones/listar/', ListarPatronesView.as_view(), name='listar-patrones'),
     
    # Router URLs (patrones/, partes/, usuarios/)
    path('', include(router.urls)),
    path('api/patron/<int:patron_id>/svg/', patron_svg_view, name='patron_svg'),
]