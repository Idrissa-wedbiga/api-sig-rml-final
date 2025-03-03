from django.db import models

# Create your models here.
class Materiel(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=50)
    quantite = models.PositiveIntegerField(blank=True, null=True)
    laboratoire = models.ForeignKey("Laboratoire.Laboratoire", on_delete=models.CASCADE)
    ETAT_CHOICES = [
        ("Disponible", "Disponible"),
        ("Maintenance", "En maintenance"),
        ("Hors_service", "Hors Service"),
    ]
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default="Disponible")
    mutualisable = models.BooleanField(default=False)
    image = models.ImageField(upload_to="materiels/images/", blank=True, null=True)

    def __str__(self):
        return self.nom
