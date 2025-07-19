from django.test import TestCase
from .models import Usuario
from .utils import generar_token_activacion

class AccountActivationTestCase(TestCase):
    def setUp(self):
        Usuario.objects.create_user(correo_electronico="testuser", nombre="usuario", password="12345")
    def test_activation_success(self):
        token = generar_token_activacion(Usuario.objects.get(nombre="usuario").correo_electronico)
        response = self.client.get(f"/auth/activate/{token}/")
        self.assertEqual(response.status_code, 200)
    def test_activation_failure(self):
        response = self.client.get(f"/auth/activate/token_falso28ch8j8i32/")
        self.assertEqual(response.status_code, 400)


class UserTestCase(TestCase):
    def test_user_creation(self):
        user = Usuario.objects.create_user(correo_electronico="testuser", nombre="usuario", password="12345")
        self.assertIsNotNone(user.id)

class LoginTestCase(TestCase):

    def setUp(self):
        Usuario.objects.create_superuser(correo_electronico="testuser", nombre="usuario", password="12345")
        
    def test_login_success(self):
        response = self.client.post("/auth/login/", {"correo_electronico": "testuser", "password": "12345"})
        self.assertEqual(response.status_code, 200)  

    def test_login_failure(self):
        response = self.client.post("/auth/login/", {"correo_electronico": "wrong", "password": "wrong"})
        self.assertEqual(response.status_code, 401)