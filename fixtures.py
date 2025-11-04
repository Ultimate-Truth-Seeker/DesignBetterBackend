from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from ecommerce.models import EstadoPedido
from patronaje.models import PlantillaPrenda


EstadoPedido.objects.create(
    slug='pendiente', nombre='Pendiente', orden=1
)
EstadoPedido.objects.create(
    slug='diseno', nombre='En Diseño', orden=2
)
EstadoPedido.objects.create(
    slug='produccion', nombre='Producción', orden=3
)
#PlantillaPrenda.objects.create(nombre = "plantilla ejemplo", descripcion = "", tipo_ropa = "", tipo_cuerpo = "")
#TODO Pendiente añadir plantilla nueva de ejemplo