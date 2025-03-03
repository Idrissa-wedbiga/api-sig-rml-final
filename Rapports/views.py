from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Rapports.models import Rapport, Historique
from Rapports.permissions import IsResponsableLaboratoire
from Rapports.serializers import RapportSerializer, HistoriqueSerializer
from usersManagements.permissions import IsAdmin
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser

# Create your views here.
#Create
class RapportCreateAPIView(APIView):    
    serializer_class = RapportSerializer
    parser_classes = [JSONParser]
    #permission_classes = [IsResponsableLaboratoire]
    @swagger_auto_schema(request_body=RapportSerializer, operation_description="Créer un rapport", responses={201: RapportSerializer, 400: "Mauvaise requête"})
    def post(self, request, format=None):
        serializer = RapportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Read
class RapportListAPIView(APIView):
    #permission_classes = [IsAdmin]  # Utilisez une combinaison de permissions
    def get(self, request, format=None):
        rapports = Rapport.objects.all()
        serializer = RapportSerializer(rapports, many=True)
        return Response(serializer.data)
#Detail rapport
class RapportDetailAPIView(APIView):
    #permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return Rapport.objects.get(pk=pk)
        except Rapport.DoesNotExist:
            return None
    def get(self, request, pk, format=None):
        rapport = self.get_object(pk)
        if rapport is None:
            return Response({"error": "Rapport non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RapportSerializer(rapport)
        return Response(serializer.data)
#Update
class RapportUpdateAPIView(APIView):
    #permission_classes = [IsResponsableLaboratoire]
    @swagger_auto_schema(request_body=RapportSerializer, operation_description="Modifier un rapport", responses={200: RapportSerializer, 400: "Mauvaise requête"})
    def put(self, request, pk, format=None):
        rapport = self.get_object(pk)
        if rapport is None:
            return Response({"error": "Rapport non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RapportSerializer(rapport, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Delete
class RapportDeleteAPIView(APIView):
    #permission_classes = [IsAdmin]
    def delete(self, request, pk, format=None):
        rapport = self.get_object(pk)
        if rapport is None:
            return Response({"error": "Rapport non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        rapport.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#Historique
class HistoriqueListAPIView(APIView):
    #permission_classes = [IsAdmin]
    def get(self, request, format=None):
        historiques = Historique.objects.all()
        serializer = HistoriqueSerializer(historiques, many=True)
        return Response(serializer.data)
    
#Create
class HistoriqueCreateAPIView(APIView):
    #permission_classes = [IsAdmin]
    @swagger_auto_schema(request_body=HistoriqueSerializer, operation_description="Créer un historique", responses={201: HistoriqueSerializer, 400: "Mauvaise requête"})
    def post(self, request, format=None):
        serializer = HistoriqueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
#Detail Historique
class HistoriqueDetailAPIView(APIView):
    #permission_classes = [IsAdmin]
    def get_object(self, pk):
        try:
            return Historique.objects.get(pk=pk)
        except Historique.DoesNotExist:
            return None
        
    def get(self, request, pk, format=None):
        historique = self.get_object(pk)
        if historique is None:
            return Response({"error": "Historique non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = HistoriqueSerializer(historique)
        return Response(serializer.data)
    
#Update
class HistoriqueUpdateAPIView(APIView):
    #permission_classes = [IsAdmin]
    @swagger_auto_schema(request_body=HistoriqueSerializer, operation_description="Modifier un historique", responses={200: HistoriqueSerializer, 400: "Mauvaise requête"})
    def put(self, request, pk, format=None):
        historique = self.get_object(pk)
        if historique is None:
            return Response({"error": "Historique non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = HistoriqueSerializer(historique, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Delete
class HistoriqueDeleteAPIView(APIView):
    #permission_classes = [IsAdmin]
    def delete(self, request, pk, format=None):
        historique = self.get_object(pk)
        if historique is None:
            return Response({"error": "Historique non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        historique.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
