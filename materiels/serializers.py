from rest_framework import serializers
from .models import Materiel

class MaterielSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materiel
        fields = '__all__'