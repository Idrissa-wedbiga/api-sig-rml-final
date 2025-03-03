# tests.py
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .permissions import IsResponsableLaboratoire

class IsResponsableLaboratoireTest(TestCase):
    def setUp(self):
        self.permission = IsResponsableLaboratoire()
        self.factory = RequestFactory()

    def test_authenticated_user_with_correct_role(self):
        user = User.objects.create_user(username="testuser", role="RESPONSABLE-LABORATOIRE")
        request = self.factory.get("/api/")
        request.user = user
        self.assertTrue(self.permission.has_permission(request, None))

    def test_authenticated_user_with_wrong_role(self):
        user = User.objects.create_user(username="testuser", role="AUTRE-ROLE")
        request = self.factory.get("/api/")
        request.user = user
        self.assertFalse(self.permission.has_permission(request, None))

    def test_unauthenticated_user(self):
        request = self.factory.get("/api/")
        request.user = None
        self.assertFalse(self.permission.has_permission(request, None))