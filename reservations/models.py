from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ValidationError
from usersManagements.models import Utilisateur
from materiels.models import Materiel

# Create your models here.
class Reservation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    motif = models.TextField()
    STATUT_CHOICES = [
        ("en_attente", "En attente"),
        ("validee", "Validée"),
        ("annulee", "Annulée"),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="en_attente")

    def __str__(self):
        return f"{self.utilisateur.username} - {self.materiel.name} - {self.date_debut}"

    def clean(self):
        overlapping_reservations = Reservation.objects.filter(
            materiel=self.materiel,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
            status='Validée'
        ).exclude(id=self.id)

        if overlapping_reservations.exists():
            raise ValidationError("L'équipement est déjà réservé pour cette plage horaire.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
        
class Notification(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.user.email} - {self.reservation} - {self.date_envoi}: {self.message[:50]}"
    
    @receiver(post_save, sender=Reservation)
    def send_reservation_notification(sender, instance, created, **kwargs):
        if created:
            message = f"Votre réservation pour {instance.materiel.name} a été créée."
        else:
            message = f"Votre réservation pour {instance.materiel.name} a été mise à jour."
    
        Notification.objects.create(user=instance.user, message=message)