from rest_framework import permissions
from .constants import ROLE_RESPONSABLE_LABORATOIRE

class IsResponsableLaboratoire(permissions.BasePermission):
    """ Permission pour les responsables de laboratoire uniquement """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == ROLE_RESPONSABLE_LABORATOIRE

    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est responsable du laboratoire lié à cet objet
        return request.user.role == ROLE_RESPONSABLE_LABORATOIRE and obj.laboratoire.responsable == request.user