from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from ecommerce.models import EstadoPedido
from designbetter.models import PlantillaPrenda

site = Site.objects.get(id=1)

app = SocialApp.objects.create(
    provider='google',
    name='Google Login',
    client_id='454329887491-3vjn6t36k4c45l2l3n96k87gl77v5jjq.apps.googleusercontent.com',
    secret='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'
)
app.sites.add(site)

EstadoPedido.objects.create(
    slug='pendiente', nombre='Pendiente', orden=1
)
EstadoPedido.objects.create(
    slug='diseno', nombre='En Diseño', orden=2
)
EstadoPedido.objects.create(
    slug='produccion', nombre='Producción', orden=3
)
PlantillaPrenda.objects.create(nombre = "plantilla ejemplo", descripcion = "", tipo_ropa = "", tipo_cuerpo = "")