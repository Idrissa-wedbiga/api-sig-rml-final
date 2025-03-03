from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reservations.models import Reservation, Notification
from reservations.permissions import IsResponsableLaboratoire
from reservations.serializers import ReservationSerializer
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger(__name__)

    
def envoyer_email_notification(email, sujet, message):
    send_mail(
        sujet,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Expéditeur (défini dans settings.py)
        [email],  # Destinataire
        fail_silently=False,
    )
# Créer une réservation
class FaireUneReservationView(APIView):
    #permission_classes = [IsResponsableLaboratoire]
    @swagger_auto_schema(request_body=ReservationSerializer, operation_description="Créer une reservation", responses={201: ReservationSerializer, 400: "Mauvaise requête"})
    def post(self, request):
        serializer = ReservationSerializer(data=request.data)  # ✅ Utiliser le serializer

        if serializer.is_valid():
            reservation = serializer.save()  # ✅ Enregistre les données validées

            # ✅ Récupérer l'utilisateur (relation ForeignKey)
            utilisateur = reservation.utilisateur

            # ✅ Création d'une notification
            Notification.objects.create(
                utilisateur=utilisateur,
                message=f"Votre réservation pour {reservation.materiel} a été effectuée du {reservation.date_debut} au {reservation.date_fin}."
            )

            # ✅ Envoi d'un email
            envoyer_email_notification(
                utilisateur.email,
                "Confirmation de réservation",
                f"Bonjour {utilisateur.name},\n\nVotre réservation de {reservation.materiel} du {reservation.date_debut} au {reservation.date_fin} a bien été prise en compte."
            )

            return Response({
                "message": "Réservation effectuée avec succès et notification envoyée.",
                "reservation": serializer.data  # ✅ Retourner la réservation sérialisée
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # ✅ Gestion des erreur

# Accepter une reservation
class AccepterUneReservationView(APIView):
    #permission_classes = [IsResponsableLaboratoire]
    @swagger_auto_schema(request_body=ReservationSerializer, operation_description="Accepter une reservation", responses={200: ReservationSerializer, 400: "Mauvaise requête"})
    def post(self, request):
        id = request.data.get('id')
        if not id:
            return Response({"error": "L'ID de la réservation est requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Récupérez la réservation par son ID
            reservation = Reservation.objects.get(id=id)

            # Mettez à jour l'état de la réservation
            reservation.accepted = True
            reservation.save()

            # Sérialisez la réservation mise à jour
            serializer = ReservationSerializer(reservation)

            # Créez une notification
            Notification.objects.create(
                utilisateur=reservation.utilisateur,
                message=f"Votre réservation pour {reservation.materiel} a été acceptée."
            )

            # Envoyez un email de confirmation
            envoyer_email_notification(
                reservation.utilisateur.email,
                "Confirmation de réservation",
                f"Bonjour {reservation.utilisateur.name},\n\nVotre réservation de {reservation.materiel} du {reservation.date_debut} au {reservation.date_fin} a bien été acceptée."
            )

            # Retournez une réponse avec les données sérialisées
            return Response({
                "message": "Réservation acceptée.",
                "reservation": serializer.data  # Données sérialisées
            }, status=status.HTTP_200_OK)

        except Reservation.DoesNotExist:
            return Response({"error": "La réservation spécifiée n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
        
# Refuser une reservation
class RefuserUneReservationView(APIView):
    #permission_classes = [IsResponsableLaboratoire]
    @swagger_auto_schema(request_body=ReservationSerializer, operation_description="Refuser une reservation", responses={200: ReservationSerializer, 400: "Mauvaise requête"})
    def post(self, request):
        id = request.data.get('id')
        if not id:
            return Response({"error": "L'ID de la réservation est requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Récupérez la réservation par son ID
            reservation = Reservation.objects.get(id=id)

            # Mettez à jour l'état de la réservation
            reservation.accepted = False
            reservation.save()

            # Sérialisez la réservation mise à jour
            serializer = ReservationSerializer(reservation)

            # Créez une notification
            Notification.objects.create(
                utilisateur=reservation.utilisateur,
                message=f"Votre réservation pour {reservation.materiel} a été refusée."
            )

            # Envoyez un email de refus
            envoyer_email_notification(
                reservation.utilisateur.email,
                "Réservation refusée",
                f"Bonjour {reservation.utilisateur.name},\n\nVotre réservation de {reservation.materiel} du {reservation.date_debut} au {reservation.date_fin} a été refusée."
            )

            # Retournez une réponse avec les données sérialisées
            return Response({
                "message": "Réservation refusée.",
                "reservation": serializer.data  # Données sérialisées
            }, status=status.HTTP_200_OK)

        except Reservation.DoesNotExist:
            return Response({"error": "La réservation spécifiée n'existe pas."}, status=status.HTTP_404_NOT_FOUND)

# Liste des reservations
class ListeDesReservationsView(APIView):    
    def get(self, request):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

# Obtenir une reservation
class ObtenirUneReservationView(APIView):
    def get(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)
    
    
# Supprimer une reservation
class SupprimerUneReservationView(APIView):
    #@swagger_auto_schema(request_body=ReservationSerializer, operation_description="Supprimer une reservation", responses={200: "Réservation supprimée."})
    def delete(self, request):
        id = request.data.get('id')
        if not id:
            return Response({"error": "L'ID de la réservation est requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reservation = Reservation.objects.get(id=id)
            reservation.delete()
            return Response({"message": "Réservation supprimée."}, status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response({"error": "La réservation spécifiée n'existe pas."}, status=status.HTTP_404_NOT_FOUND)