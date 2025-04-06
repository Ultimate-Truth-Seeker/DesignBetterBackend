from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),  
    path('redireccion/', views.redireccionar_por_rol, name='redireccionar_por_rol'),
]