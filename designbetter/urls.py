from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from .views import RegistroView, ActivarCuentaView, PasswordResetRequestView, PasswordResetConfirmView, UsuarioViewSet, CustomTokenObtainPairView, GoogleLogin, AsignarRolView, DxfFileUploadView


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistroView.as_view(), name='register'),
    path('activate/<token>/', ActivarCuentaView.as_view(), name='activar_cuenta'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_api'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm_api'),
    path('social/google/', GoogleLogin.as_view(), name='google_login'),

    path("asignar-rol/", AsignarRolView.as_view(), name="asignar-rol"),
    path('upload-dxf/', DxfFileUploadView.as_view(), name='upload-dxf'),

]