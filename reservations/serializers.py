from rest_framework import serializers
from .models import Reservation, Notification
from usersManagements.serializers import UtilisateurSerializer
from materiels.serializers import MaterielSerializer

class ReservationSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer(read_only=True)
    materiel = UtilisateurSerializer(read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'
        
class NotificationSerializer(serializers.ModelSerializer):      
    class Meta:
        model = Notification
        fields = '__all__'