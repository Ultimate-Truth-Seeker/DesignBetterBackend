from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

User = get_user_model()

class AuthIntegrationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            correo_electronico="ana@example.com", password="SuperSecreta123", nombre="nombre_usuario"
        )
        cls.user.is_active = True
        cls.user.save()

    def setUp(self):
        self.client = APIClient()

    def test_login_and_access_protected(self):
        # Ajusta la ruta al login de tu API (token/jwt/session)
        res_login = self.client.post("/auth/login/", {
            "correo_electronico": "ana@example.com",
            "password": "SuperSecreta123"
        }, format="json")
        self.assertEqual(res_login.status_code, status.HTTP_200_OK)
        token = res_login.data.get("access")
        self.assertIsNotNone(token)

        # Usa el token para acceder a un endpoint protegido
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res_me = self.client.get("/orders/pedidos/")
        self.assertEqual(res_me.status_code, status.HTTP_200_OK)

from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from ecommerce.models import PlantillaPrenda as Product, EstadoPedido  # ajusta import según tu proyecto


class OrderIntegrationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.user = User.objects.create_user(correo_electronico="ana@example.com", password="x", nombre="usuario")
        cls.user.is_active = True
        cls.user.save()
        cls.estado_pendiente = EstadoPedido.objects.create(
            slug='pendiente', nombre='Pendiente', orden=1
        )
        cls.p1 = Product.objects.create(nombre="plantilla1", descripcion="texto", tipo_ropa="ejemplo", tipo_cuerpo="XL")
        #cls.p2 = Product.objects.create(nombre="plantilla", descripcion="texto", tipo_ropa="ejemplo", tipo_cuerpo="XL")
    

    def setUp(self):
        self.client = APIClient()
        res_login = self.client.post("/auth/login/", {
            "correo_electronico": "ana@example.com",
            "password": "SuperSecreta123"
        }, format="json")
        self.token = res_login.data.get("access")

    def test_create_orders(self):
        payload = {
            "plantilla": 1,    # asume que existen IDs válidos
            "disenador": 1,
            "color": "Rojo",
            "ajustes": "Sin ajuste",
            "notas": "Prueba"
        }
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        res = self.client.post("/orders/pedidos/crear/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

User = get_user_model()

class ProductListIntegrationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u = User.objects.create_user(correo_electronico="ana@example.com", password="x", nombre="usuario")
        names = [f"Producto {i:02d}" for i in range(1, 26)]
        for i, name in enumerate(names, start=1):
            Product.objects.create(nombre=f"{name}{i}", descripcion="texto", tipo_ropa="ejemplo", tipo_cuerpo="XL")

    def setUp(self):
        self.client = APIClient()
        self.client = APIClient()
        res_login = self.client.post("/auth/login/", {
            "correo_electronico": "ana@example.com",
            "password": "SuperSecreta123"
        }, format="json")
        self.token = res_login.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.client.force_authenticate(user=self.u)

    def test_paginated_list(self):
        # Suponiendo page_size=10 en tu paginador DRF
        res = self.client.get("/orders/pedidos/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
