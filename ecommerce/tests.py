from django.test import TestCase

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework import status
from django.contrib.auth.models import Group
from .models import (
    Usuario,
    PlantillaPrenda,
    EstadoPedido,
    PedidoPersonalizado,
    PedidoEstadoHistoria
)

class PedidoPersonalizadoTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Grupos
        clientes, _ = Group.objects.get_or_create(name='Clientes')
        diseniadores, _ = Group.objects.get_or_create(name='Diseñadores')

        # Usuarios
        cls.cliente = Usuario.objects.create_user(
            correo_electronico='cli@example.com',
            nombre='Cliente Uno',
            password='pass123',
            rol='cliente'
        )
        cls.cliente.is_active = True
        cls.cliente.save()
        cls.cliente.groups.add(clientes)

        cls.disenador = Usuario.objects.create_user(
            correo_electronico='dise@example.com',
            nombre='Diseñador Uno',
            password='pass123',
            rol='diseñador'
        )
        cls.disenador.is_active = True
        cls.disenador.save()
        cls.disenador.groups.add(diseniadores)
    
        cls.plantilla = PlantillaPrenda.objects.create(nombre="plantilla", descripcion="texto", tipo_ropa="ejemplo", tipo_cuerpo="XL")

        # Estados
        cls.estado_pendiente = EstadoPedido.objects.create(
            slug='pendiente', nombre='Pendiente', orden=1
        )
        cls.estado_diseno = EstadoPedido.objects.create(
            slug='diseno', nombre='En Diseño', orden=2
        )
        cls.estado_produccion = EstadoPedido.objects.create(
            slug='produccion', nombre='Producción', orden=3
        )
    def authenticate(self, email, password):
        url = reverse('token_obtain_pair')  # o el nombre de tu CustomTokenObtainPairView
        resp = self.client.post(url, {
            'correo_electronico': email,
            'password': password
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def setUp(self):
        self.client = APIClient()

    def test_cliente_crea_pedido_con_estado_pendiente_y_pago_falso(self):
        self.authenticate('cli@example.com', 'pass123')
        url = reverse('crear-pedido')
        payload = {
            "plantilla": 1,    # asume que existen IDs válidos
            "color": "Rojo",
            "ajustes": "Sin ajuste",
            "notas": "Prueba"
        }
        resp = self.client.post(url, payload, format='json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.data
        self.assertEqual(data['estado'], 'pendiente')
        self.assertFalse(data['pago_realizado'])
        self.assertEqual(data['usuario'], self.cliente.id)

    def test_cliente_no_puede_modificar_su_pedido(self):
        # Primero creamos un pedido
        pedido = PedidoPersonalizado.objects.create(
            usuario=self.cliente,
            plantilla_id=1,
            color='Azul',
            ajustes='-',
            notas='-',
            estado=self.estado_pendiente
        )
        self.authenticate('cli@example.com', 'pass123')
        url = reverse('actualizar-estado-pedido', args=[pedido.id])
        resp = self.client.patch(url, {'estado': self.estado_diseno.id}, format='json')
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND))

    def test_disenador_modifica_estado_y_registra_historial(self):
        # Creamos pedido “dirigido” a este diseñador:
        pedido = PedidoPersonalizado.objects.create(
            usuario=self.cliente,
            plantilla_id=1,
            color='Negro',
            ajustes='-',
            notas='-',
            estado=self.estado_pendiente
        )
        self.authenticate('dise@example.com', 'pass123')
        url = reverse('actualizar-estado-pedido', args=[pedido.id])

        # Cambiamos el estado
        resp = self.client.patch(url, {'estado': self.estado_produccion.id}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Se creó un historial
        historial = PedidoEstadoHistoria.objects.filter(pedido=pedido)
        self.assertEqual(historial.count(), 1)
        entry = historial.first()
        self.assertEqual(entry.estado, self.estado_produccion)
        self.assertEqual(entry.usuario, self.disenador)

    def test_disenador_valida_pago(self):
        pedido = PedidoPersonalizado.objects.create(
            usuario=self.cliente,
            plantilla_id=1,
            color='Verde',
            ajustes='-',
            notas='-',
            estado=self.estado_pendiente
        )
        self.authenticate('dise@example.com', 'pass123')
        url = reverse('actualizar-pago-pedido', args=[pedido.id])

        resp = self.client.patch(url, {'pago_realizado': True}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        pedido.refresh_from_db()
        self.assertTrue(pedido.pago_realizado)

    def test_usuario_ve_solo_sus_pedidos(self):
        # Otro cliente crea un pedido
        otro = Usuario.objects.create_user(
            correo_electronico='cli2@example.com',
            nombre='Cliente Dos',
            password='pass123',
            rol='cliente'
        )
        otro.is_active=True; otro.save()
        pedido = PedidoPersonalizado.objects.create(
            usuario=self.cliente,
            plantilla_id=1,
            color='Blanco',
            ajustes='-',
            notas='-',
            estado=self.estado_pendiente
        )
        pedido_otro = PedidoPersonalizado.objects.create(
            usuario=otro,
            plantilla_id=1,
            color='Blanco',
            ajustes='-',
            notas='-',
            estado=self.estado_pendiente
        )

        # Cliente original pide lista
        self.authenticate('cli@example.com', 'pass123')
        url = reverse('historial-pedido', args=[pedido.id])  # asume que tienes un ListAPIView
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Todos los pedidos devueltos deben pertenecer a self.cliente
        for item in resp.data:
            self.assertEqual(item['usuario'], self.cliente.id)