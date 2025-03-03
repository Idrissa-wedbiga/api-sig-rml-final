from rest_framework import permissions

class IsResponsableLaboratoire(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "RESPONSABLE-LABORATOIRE"
    
class IsEnseignantChercheur(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ENSEIGNANT-CHERCHEUR"
    
class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "STUDENT"