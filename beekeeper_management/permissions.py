from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    """
    Permite el acceso solo a usuarios con el rol 'admin' o que sean superusuarios.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.role == "admin" or request.user.is_superuser)
