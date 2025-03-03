from rest_framework import serializers
from .models import Laboratoire

class LaboratoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratoire
        fields = ['id', 'nom', 'responsable', 'date_creation', 'description']