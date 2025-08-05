from django.test import TestCase
from .models import Usuario
from .utils import generar_token_activacion
import re
from django.core import mail
from django.core.signing import Signer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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

# Prueba de funcionalidad: Registro e inicio de Sesion
# tests/test_auth_flow.py
class RegistroLoginFlowTest(APITestCase):
    def setUp(self):
        # Rutas (cámbialas si usas otros names en urls.py)
        self.register_url  = reverse('register')            # /auth/register/
        self.token_url     = reverse('token_obtain_pair')   # /auth/token/
        # Activación será f"/auth/activate/{token}/" – se forma en el test

        # Datos de usuario
        self.user_data = {
            'correo_electronico': 'cliente@example.com',
            'nombre': 'Cliente Demo',
            'password': 'Segura123!',
            'rol': 'cliente',
        }

    def test_registro_activacion_login_ok(self):
        # 1️⃣ REGISTRO ---------------------------------------------------------
        resp = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Se envió exactamente 1 correo
        self.assertEqual(len(mail.outbox), 1)

        # 2️⃣ EXTRAER TOKEN DE CORREO -----------------------------------------
        mensaje = mail.outbox[0].body
        m = re.search(r'/activate/(?P<token>[^/]+)/', mensaje)
        self.assertIsNotNone(m, f'No se encontró token en el correo {mensaje}')
        token = m.group('token')

        # 3️⃣ ACTIVAR CUENTA ---------------------------------------------------
        activate_url = reverse('activar_cuenta', kwargs={'token': token})
        resp = self.client.get(activate_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('Cuenta activada', resp.data['detail'])

        # 4️⃣ LOGIN / OBTENER JWT ---------------------------------------------
        login_payload = {
            'correo_electronico': self.user_data['correo_electronico'],
            'password': self.user_data['password'],
        }
        resp = self.client.post(self.token_url, login_payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access',  resp.data)
        self.assertIn('refresh', resp.data)
        self.assertEqual(resp.data['email'], self.user_data['correo_electronico'])
        self.assertEqual(resp.data['nombre'], self.user_data['nombre'])
        self.assertEqual(resp.data['rol'],    self.user_data['rol'])

    def test_login_falla_sin_activar(self):
        # Registro, pero sin activar
        self.client.post(self.register_url, self.user_data, format='json')

        login_payload = {
            'correo_electronico': self.user_data['correo_electronico'],
            'password': self.user_data['password'],
        }
        resp = self.client.post(self.token_url, login_payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_registro_falla_con_correo_usado(self):
        # Registro, pero sin activar
        resp = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Registro usando los mismos datos
        resp = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(resp.status_code, 400)