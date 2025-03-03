from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from usersManagements.models import Utilisateur
from usersManagements.permissions import IsAdmin
from usersManagements.serializers import UtilisateurSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema


# ✅ Classe de connexion avec Token
class LoginView(APIView):
    #permission_classes = [AllowAny]  # Tout le monde peut se connecter
    @swagger_auto_schema(request_body=UtilisateurSerializer, operation_description="Connexion", responses={200: "Token", 400: "Mauvaise requête"})
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email et mot de passe sont obligatoires."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier l'authentification
        user = authenticate(username=email, password=password)  # Django attend 'username', même si c'est un email

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user_id": user.id, "email": user.email, "role": user.role}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)

# Classe de déconnexion avec suppression du token
class LogoutView(APIView):
    #authentication_classes = [TokenAuthentication]  # Seuls les utilisateurs authentifiés peuvent se déconnecter
    @swagger_auto_schema(request_body=UtilisateurSerializer, operation_description="Déconnexion", responses={200: "Déconnexion", 400: "Mauvaise requête"})
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except AttributeError:
            return Response({"error": "Aucun token trouvé."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK)


# Classe de mise à jour du mot de
class UpdatePasswordView(APIView):
    #authentication_classes = [TokenAuthentication]  # Seuls les utilisateurs authentifiés peuvent mettre à jour leur mot de passe
    @swagger_auto_schema(request_body=UtilisateurSerializer, operation_description="Mise à jour du mot de passe", responses={200: "Mot de passe mis à jour.", 400: "Mauvaise requête"})
    def put(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email et mot de passe sont obligatoires."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier l'authentification
        user = authenticate(username=email, password=password)  # Django attend 'username', meme si c'est un email

        if user is not None:
            user.set_password(password)
            user.save()
            return Response({"message": "Mot de passe mis à jour."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)
        
#Create
class CreateUserView(APIView):
    #permission_classes = [IsAdmin]  # Seuls les administrateurs peuvent créer un utilisateur
    @swagger_auto_schema(request_body=UtilisateurSerializer, operation_description="Créer un utilisateur", responses={201: UtilisateurSerializer, 400: "Mauvaise requête"})
    def post(self, request):
        serializer = UtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Read
class GetAllUsersView(APIView):
    #authentication_classes = [TokenAuthentication]  # Seuls les utilisateurs authentifiés peuvent accéder à tous les utilisateurs
    def get(self, request):
        users = Utilisateur.objects.all()
        serializer = UtilisateurSerializer(users, many=True)
        return Response(serializer.data)
# ✅ Classe de récupération des informations d'un utilisateur
class UtilisateurDetailView(APIView):
    #permission_classes = [TokenAuthentication]  # Seuls les utilisateurs authentifiés peuvent accéder à un utilisateur

    def get_object(self, pk):
        try:
            return Utilisateur.objects.get(pk=pk)
        except Utilisateur.DoesNotExist:
            return None
    def get(self, request, pk, format=None):
        
        utilisateur = self.get_object(pk)
        if utilisateur is None:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UtilisateurSerializer(utilisateur)
        return Response(serializer.data)
# Classe de mise à jour d'un utilisateur
class UtilisateurUpdateView(APIView):
    #permission_classes = [TokenAuthentication]  # ✅ Seuls les utilisateurs authentifiés peuvent mettre à jour un utilisateur

    def get_object(self, pk):
        try:
            return Utilisateur.objects.get(pk=pk)
        except Utilisateur.DoesNotExist:
            return None
    @swagger_auto_schema(request_body=UtilisateurSerializer, operation_description="Modifier un utilisateur", responses={200: UtilisateurSerializer, 400: "Mauvaise requête"})
    def put(self, request, pk, format=None):
        utilisateur = self.get_object(pk)
        if utilisateur is None:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UtilisateurSerializer(utilisateur, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Classe de suppression d'un utilisateur
class UtilisateurDeleteView(APIView):
    #permission_classes = [TokenAuthentication]  # Seuls les utilisateurs authentifiés peuvent supprimer un utilisateur

    def get_object(self, pk):
        try:
            return Utilisateur.objects.get(pk=pk)
        except Utilisateur.DoesNotExist:
            return None
    @swagger_auto_schema(request_body=UtilisateurSerializer, operation_description="Supprimer un utilisateur", responses={204: "Utilisateur supprimé.", 400: "Mauvaise requête"})
    def delete(self, request, pk, format=None):
        utilisateur = self.get_object(pk)
        if utilisateur is None:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        utilisateur.delete()
        return Response({"message": "Utilisateur supprimé."}, status=status.HTTP_204_NO_CONTENT)