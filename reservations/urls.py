from django.urls import path
from . views import (
    FaireUneReservationView,
    AccepterUneReservationView,
    RefuserUneReservationView,
    ListeDesReservationsView,
    ObtenirUneReservationView,
    SupprimerUneReservationView,
)


urlpatterns = [
    path('faire/', FaireUneReservationView.as_view(), name='faire_reservation'),
    path('accepter/<int:pk>/', AccepterUneReservationView.as_view(), name='accepter_reservation'),
    path('refuser/<int:pk>/', RefuserUneReservationView.as_view(), name='refuser_reservation'),
    path('liste/', ListeDesReservationsView.as_view(), name='liste_reservations'),
    path('obtenir/<int:pk>/', ObtenirUneReservationView.as_view(), name='obtenir_reservation'),
    path('supprimer/<int:pk>/', SupprimerUneReservationView.as_view(), name='supprimer_reservation'),
]