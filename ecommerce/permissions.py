# permissions.py
from rest_framework import permissions

class IsCliente(permissions.BasePermission):
    """
    Permite acceso solo a usuarios autenticados con rol 'cliente'.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.rol == 'cliente'
        )

class IsDisenador(permissions.BasePermission):
    """
    Permite acceso solo a usuarios autenticados con rol 'diseñador'.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.rol == 'diseñador'
        )