from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Laboratoire


# Create your tests here.
class LaboratoireCreateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword", role="ADMIN")

    def test_create_laboratoire_authenticated(self):
        """ Vérifie que l'utilisateur authentifié peut créer un laboratoire """
        self.client.force_authenticate(user=self.user)
        data = {'nom': 'Nouveau Labo', 'description': 'Description du nouveau labo'}
        response = self.client.post('/api/laboratoires/create/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Laboratoire.objects.count(), 1)
        self.assertEqual(Laboratoire.objects.first().nom, 'Nouveau Labo')

    def test_create_laboratoire_unauthenticated(self):
        """ Vérifie que l'utilisateur non authentifié ne peut pas créer un laboratoire """
        data = {'nom': 'Nouveau Labo', 'description': 'Description du nouveau labo'}
        response = self.client.post('/api/laboratoires/create/', data, format='json')
        self.assertEqual(response.status_code, 401)  # Ou 403 selon vos permissions
class LaboratoireListAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword", role="ADMIN")
        self.laboratoire1 = Laboratoire.objects.create(nom="Labo A", description="Description A")
        self.laboratoire2 = Laboratoire.objects.create(nom="Labo B", description="Description B")

    def test_list_laboratoires_authenticated(self):
        """ Vérifie que l'utilisateur authentifié peut lister les laboratoires """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/laboratoires/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_laboratoires_unauthenticated(self):
        """ Vérifie que l'utilisateur non authentifié ne peut pas lister les laboratoires """
        response = self.client.get('/api/laboratoires/')
        self.assertEqual(response.status_code, 401)  # Ou 403 selon vos permissions
class LaboratoireDetailAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword", role="ADMIN")
        self.laboratoire = Laboratoire.objects.create(nom="Labo A", description="Description A")

    def test_retrieve_laboratoire_authenticated(self):
        """ Vérifie que l'utilisateur authentifié peut récupérer un laboratoire spécifique """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/laboratoires/{self.laboratoire.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nom'], 'Labo A')

    def test_retrieve_laboratoire_unauthenticated(self):
        """ Vérifie que l'utilisateur non authentifié ne peut pas récupérer un laboratoire spécifique """
        response = self.client.get(f'/api/laboratoires/{self.laboratoire.id}/')
        self.assertEqual(response.status_code, 401)  # Ou 403 selon vos permissions
    
class LaboratoireUpdateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword", role="ADMIN")
        self.laboratoire = Laboratoire.objects.create(nom="Labo A", description="Description A")

    def test_update_laboratoire_authenticated(self):
        """ Vérifie que l'utilisateur authentifié peut mettre à jour un laboratoire """
        self.client.force_authenticate(user=self.user)
        data = {'nom': 'Labo Mis à Jour', 'description': 'Nouvelle description'}
        response = self.client.put(f'/api/laboratoires/{self.laboratoire.id}/update/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.laboratoire.refresh_from_db()
        self.assertEqual(self.laboratoire.nom, 'Labo Mis à Jour')

    def test_update_laboratoire_unauthenticated(self):
        """ Vérifie que l'utilisateur non authentifié ne peut pas mettre à jour un laboratoire """
        data = {'nom': 'Labo Mis à Jour', 'description': 'Nouvelle description'}
        response = self.client.put(f'/api/laboratoires/{self.laboratoire.id}/update/', data, format='json')
        self.assertEqual(response.status_code, 401)  # Ou 403 selon vos permissions
class LaboratoireDeleteAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword", role="ADMIN")
        self.laboratoire = Laboratoire.objects.create(nom="Labo A", description="Description A")

    def test_delete_laboratoire_authenticated(self):
        """ Vérifie que l'utilisateur authentifié peut supprimer un laboratoire """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/laboratoires/{self.laboratoire.id}/delete/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Laboratoire.objects.count(), 0)

    def test_delete_laboratoire_unauthenticated(self):
        """ Vérifie que l'utilisateur non authentifié ne peut pas supprimer un laboratoire """
        response = self.client.delete(f'/api/laboratoires/{self.laboratoire.id}/delete/')
        self.assertEqual(response.status_code, 401)  # Ou 403 selon vos permissions