from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegistroView, ActivarCuentaView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistroView.as_view(), name='register'),
    path('activate/<token>/', ActivarCuentaView.as_view(), name='activar_cuenta'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_api'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm_api')
]