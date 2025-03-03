from django.db import models
from django.contrib.auth import get_user_model
from reservations.models import Reservation
import pandas as pd
from django.db.models import Count, F
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now

# Create your models here.

User = get_user_model()

class Rapport(models.Model):
    TYPE_CHOICES = [
        ("STATISTIQUES", "Statistiques"),
        ("ACTIVITES", "Activités"),
        ("PREVISIONS", "Prévisions"),
    ]
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rapports")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    date_generation = models.DateTimeField(auto_now_add=True)
    fichier_pdf = models.FileField(upload_to="rapports/pdf/", blank=True, null=True)
    fichier_excel = models.FileField(upload_to="rapports/excel/", blank=True, null=True)

    def __str__(self):
        return f"Rapport {self.type} - {self.date_generation}"

    def generer_excel(self, data):
        """ Génère un fichier Excel à partir des données d'analyse """
        df = pd.DataFrame(data)
        filename = f"rapport_{self.id}.xlsx"
        filepath = f"media/rapports/excel/{filename}"
        df.to_excel(filepath, index=False)
        self.fichier_excel = filepath
        self.save()
        return filepath

def generer_statistiques():
    # Nombre total de réservations par matériel
    stats_reservations = Reservation.objects.values("materiel__nom").annotate(total=Count("id"))
    
    # Matériel sous-utilisé (moins de 5 réservations)
    sous_utilises = Reservation.objects.values("materiel__nom").annotate(total=Count("id")).filter(total__lt=5)

    # Création du rapport
    rapport = Rapport.objects.create(type="STATISTIQUES", utilisateur=User.objects.first())
    data = list(stats_reservations)
    rapport.generer_excel(data)
    
    return {
        "total_reservations": list(stats_reservations),
        "materiels_sous_utilises": list(sous_utilises)
    }

# Historique des actions des utilisateurs
class Historique(models.Model):
    ACTIONS = [
        ('LOGIN', 'Connexion'),
        ('LOGOUT', 'Déconnexion'),
        ('PASSWORD_RESET', 'Réinitialisation du mot de passe'),
        ('RESERVATION_CREATED', 'Réservation créée'),
        ('RESERVATION_UPDATED', 'Réservation mise à jour'),
        ('RESERVATION_DELETED', 'Réservation supprimée'),
        ('RESERVATION_ACCEPTED', 'Réservation acceptée'),
        ('RESERVATION_REJECTED', 'Réservation refusée'),
        ('EQUIPMENT_ADDED', 'Équipement ajouté'),
        ('EQUIPMENT_UPDATED', 'Équipement mis à jour'),
        ('EQUIPMENT_DELETED', 'Équipement supprimé'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="historiques")
    action = models.CharField(max_length=50, choices=ACTIONS)
    date_action = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.utilisateur} - {self.get_action_type_display()} - {self.date_action}"
    class Meta:
        verbose_name = "Historique des actions"
        verbose_name_plural = "Historique des actions"
    
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    Historique.objects.create(
        utilisateur=user,
        action="LOGIN",
        details=f"Connexion depuis {request.META.get('REMOTE_ADDR')}",
        date_action=now()
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    Historique.objects.create(
        utilisateur=user,
        action="LOGOUT",
        details=f"Déconnexion depuis {request.META.get('REMOTE_ADDR')}",
        date_action=now()
    )