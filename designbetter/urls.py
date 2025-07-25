from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import (
    PlantillaPrendaViewSet,
    RegistroView, 
    ActivarCuentaView, 
    PasswordResetRequestView, 
    PasswordResetConfirmView, 
    CustomTokenObtainPairView, 
    CustomTokenRefreshView,
    GoogleLogin, 
    FacebookLogin,  # Añadido para consistencia
    AsignarRolView, 
    DxfFileUploadView,
    PatronBaseViewSet, 
    PartePatronViewSet,
    CrearPatronView,
    ListarPatronesView,  # Nueva vista para filtros
)
from . import views

router = DefaultRouter()
router.register(r'patrones', PatronBaseViewSet, basename='patrones')  # Añadido basename
router.register(r'partes', PartePatronViewSet, basename='partes')
router.register(r'plantillas', PlantillaPrendaViewSet)

urlpatterns = [
    # Autenticación JWT
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    # Registro y activación
    path('register/', RegistroView.as_view(), name='register'),
    path('activate/<token>/', ActivarCuentaView.as_view(), name='activar_cuenta'),
    
    # Password reset
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_api'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm_api'),
    
    # Social Auth
    path('social/google/', GoogleLogin.as_view(), name='google_login'),
    path('social/facebook/', FacebookLogin.as_view(), name='facebook_login'),  # Añadido
    
    # Roles y archivos
    path('asignar-rol/', AsignarRolView.as_view(), name='asignar-rol'),
    path('upload-dxf/', DxfFileUploadView.as_view(), name='upload-dxf'),
    
    # API adicional para patrones (filtros personalizados)
    path('patrones/listar/', ListarPatronesView.as_view(), name='listar-patrones'),
     
    # Router URLs (patrones/, partes/, usuarios/)
    path('', include(router.urls)),
    path('crear-patron/', CrearPatronView.as_view(), name='crear-patron'),
    path('api/patron/<int:patron_id>/svg/', views.patron_svg_view, name='patron_svg'),

]