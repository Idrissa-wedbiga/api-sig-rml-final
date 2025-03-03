from django.db import models


class Laboratoire(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    adresse = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    # Le responsable unique du labo
    responsable = models.OneToOneField(
        'usersManagements.Utilisateur', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='Responsable'
    )

    # Tous les utilisateurs qui appartiennent au laboratoire
    utilisateurs = models.ManyToManyField("usersManagements.Utilisateur", related_name='laboratoires')

    def __str__(self):
        return self.nom
