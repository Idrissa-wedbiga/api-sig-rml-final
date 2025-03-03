
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Laboratoire
from .serializers import LaboratoireSerializer
from usersManagements.permissions import IsAdmin
from drf_yasg.utils import swagger_auto_schema
from usersManagements.models import Utilisateur

#create
class CreateLaboratoireAPIView(APIView):
    @swagger_auto_schema(
        request_body=LaboratoireSerializer,
        operation_description="Créer un laboratoire",
        responses={201: LaboratoireSerializer, 400: "Mauvaise requête"}
    )
    def post(self, request):
        data = request.data.copy()
        
        # Vérifie si un ID de responsable a été fourni
        responsable_id = data.get("responsable")
        if responsable_id:
            try:
                
                responsable = Utilisateur.objects.get(id=responsable_id)
                data["responsable"] = responsable.id  # Convertit en ID
            except Utilisateur.DoesNotExist:
                return Response({"error": "Responsable non trouvé"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LaboratoireSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Read
class LaboratoireListAPIView(APIView):
    #permission_classes = [IsAdmin]  # Utilisez une combinaison de permissions
    def get(self, request, format=None):
        laboratoires = Laboratoire.objects.all()
        serializer = LaboratoireSerializer(laboratoires, many=True)
        return Response(serializer.data)    

class LaboratoireDetailAPIView(APIView):
    #permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return Laboratoire.objects.get(pk=pk)
        except Laboratoire.DoesNotExist:
            return None
    def get(self, request, pk, format=None):
        laboratoire = self.get_object(pk)
        if laboratoire is None:
            return Response({"error": "Laboratoire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LaboratoireSerializer(laboratoire)
        return Response(serializer.data)
#Update
class LaboratoireUpdateAPIView(APIView):
    #permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return Laboratoire.objects.get(pk=pk)
        except Laboratoire.DoesNotExist:
            return None
    @swagger_auto_schema(request_body=LaboratoireSerializer, operation_description="Modifier un laboratoire", responses={200: LaboratoireSerializer, 400: "Mauvaise requête"})
    def put(self, request, pk, format=None):
        laboratoire = self.get_object(pk)
        if laboratoire is None:
            return Response({"error": "Laboratoire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LaboratoireSerializer(laboratoire, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Delete
class LaboratoireDeleteAPIView(APIView):
    #permission_classes = [IsAdmin]
    def get_object(self, pk):
        try:
            return Laboratoire.objects.get(pk=pk)
        except Laboratoire.DoesNotExist:
            return None
    def delete(self, request, pk, format=None):
        laboratoire = self.get_object(pk)
        if laboratoire is None:
            return Response({"error": "Laboratoire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        laboratoire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
