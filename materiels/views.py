from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from materiels.models import Materiel
from materiels.permissions import IsResponsableLaboratoire
from materiels.serializers import MaterielSerializer
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger(__name__)

# Create your views here.
#Create
class AjouterMaterielView(APIView):
    #permission_classes = [IsResponsableLaboratoire]
    @swagger_auto_schema(request_body=MaterielSerializer, operation_description="Ajouter un materiel", responses={201: MaterielSerializer, 400: "Mauvaise requête"})
    def post(self, request):
        logger.info("Requête POST reçue pour ajouter un matériel.")
        serializer = MaterielSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Matériel ajouté avec succès : {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Erreur de validation : {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Read
class ListeMaterielsView(APIView):
    def get(self, request):
        logger.info("Requête GET reçue pour obtenir la liste des materiels.")
        materiels = Materiel.objects.all()
        serializer = MaterielSerializer(materiels, many=True)
        logger.info(f"Liste des materiels obtenue avec sucees : {serializer.data}")
        return Response(serializer.data)
    
class ListeMaterielIdView(APIView):
    def get(self, request, pk):
        logger.info("Requête GET reçue pour obtenir un materiel.")
        materiel = Materiel.objects.get(pk=pk)
        serializer = MaterielSerializer(materiel)
        logger.info(f"Matériel obtenu avec sucees : {serializer.data}")
        return Response(serializer.data)
    
#Update
class ModifierMaterielView(APIView):
    #permission_classes = [IsResponsableLaboratoire]
    @swagger_auto_schema(request_body=MaterielSerializer, operation_description="Modifier un materiel", responses={200: MaterielSerializer, 400: "Mauvaise requête"})
    def put(self, request, pk):
        logger.info("Requête PUT reçue pour modifier un materiel.")
        materiel = Materiel.objects.get(pk=pk)
        serializer = MaterielSerializer(materiel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Matériel modifié avec sucees : {serializer.data}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error(f"Erreur de validation : {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Delete
class SupprimerMaterielView(APIView):
    permission_classes = [IsResponsableLaboratoire]
    def delete(self, request, pk):
        logger.info("Requête DELETE reçue pour supprimer un materiel.")
        materiel = Materiel.objects.get(pk=pk)
        materiel.delete()
        logger.info(f"Matériel supprimé avec sucees.")
        return Response(status=status.HTTP_204_NO_CONTENT)
