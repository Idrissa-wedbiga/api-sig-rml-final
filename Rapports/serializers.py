from rest_framework import serializers
from .models import Rapport, Historique

class RapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rapport
        fields = '__all__'
        
class HistoriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historique
        fields = '__all__'