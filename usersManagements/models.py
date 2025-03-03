from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Crée et enregistre un utilisateur avec l'email et le mot de passe fournis.
        """
        if not email:
            raise ValueError('The Email must be set')
        #Normalise l'email (met en minuscule la partie avant le @)
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crée et enregistre un superutilisateur avec l'email et le mot de passe fournis.
        """
        # Définit les valeurs par défaut pour un superutilisateur
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # Vérifie que les champs obligatoires pour un superutilisateur sont définis
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Le superutilisateur doit avoir is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Le superutilisateur doit avoir is_superuser=True."))

        # Crée le superutilisateur en utilisant la méthode create_user
        return self.create_user(email, password, **extra_fields)
    
class Utilisateur(AbstractUser):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=False)
    matricule = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=50, 
                            choices=[
                                ("admin", "Admin"), 
                                ("user", "User"), 
                                ("responsable", "Responsable")
                                
                                ], 
                            default="user")
   

    date_inscription = models.DateField(auto_now_add=True)
# Utilisez l'email comme identifiant pour l'authentification
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","username", "matricule", "password"]  # Champs obligatoires pour la commande createsuperuser

    # Associez le CustomUserManager au modèle
    objects = CustomUserManager()

    def __str__(self):
        return self.email


