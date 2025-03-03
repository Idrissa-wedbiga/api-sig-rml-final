from rest_framework import serializers
from .models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'name', 'username', 'email', 'matricule', 'password', 'role', 'date_inscription']
        extra_kwargs = {
            'password': {'write_only': True}  # Empêche le mot de passe d'être lu
        }

    def create(self, validated_data):
        """Créer un utilisateur avec un mot de passe hashé"""
        user = Utilisateur.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            username=validated_data['username'],
            matricule=validated_data['matricule'],
            role=validated_data['role']
        )
        return user

    def update(self, instance, validated_data):
        """Mettre à jour un utilisateur, en gérant correctement le mot de passe"""
        password = validated_data.pop('password', None)  # Retirer le mot de passe des autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # Hash le mot de passe
        instance.save()
        return instance
