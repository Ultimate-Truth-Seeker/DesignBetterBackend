from django.urls import path
from .views import UsuarioAdminAPIView

urlpatterns = [
    path('usuarios/', UsuarioAdminAPIView.as_view(), name='api-usuarios-admin'),
]