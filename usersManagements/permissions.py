from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """ Permission pour les administrateurs uniquement """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"
