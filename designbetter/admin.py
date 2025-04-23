from django.contrib import admin
from .models import Usuario
from .models import PatronBase
from .models import PlantillaPrenda
from .models import Material
from .models import PlantillaMaterial
from .models import PartePatron

#admin.site.register(Usuario)

from django.urls import path
from django.template.response import TemplateResponse
from django.db.models.functions import TruncMonth
from django.db.models import Count
from allauth.socialaccount.models import SocialAccount
from django.utils.timezone import now, timedelta



class MiAdmin(admin.AdminSite):
    site_header = "Panel de Administración Avanzado"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('estadisticas/', self.admin_view(self.estadisticas_view), name="estadisticas")
        ]
        return custom_urls + urls

    def estadisticas_view(self, request):
        total_usuarios = Usuario.objects.count()
        activos = Usuario.objects.filter(is_active=True).count()
        usuarios_por_mes = (
            Usuario.objects.annotate(mes=TruncMonth("fecha_creacion"))
            .values("mes")
            .annotate(total=Count("id"))
            .order_by("mes")
        )
        usuarios_por_proveedor = (
            SocialAccount.objects.values('provider')
            .annotate(total=Count('id'))
        )
        hace_7_dias = now() - timedelta(days=7)
        nuevos_recientes = Usuario.objects.filter(fecha_creacion__gte=hace_7_dias).count()
        autenticados = Usuario.objects.exclude(last_login=None).count()
        return TemplateResponse(request, "admin/estadisticas.html", {
            "total_usuarios": total_usuarios,
            "activos": activos,
            "ahora": now(),
            "usuario_por_mes": usuarios_por_mes,
            "usuario_por_proveedor": usuarios_por_proveedor,
            "nuevos_recientes": nuevos_recientes,
            "autenticados": autenticados
        })
        

admin_site = MiAdmin(name='miadmin')

admin_site.register(Usuario)
admin_site.register(PatronBase)
admin_site.register(PlantillaPrenda)
admin_site.register(Material)
admin_site.register(PlantillaMaterial)
admin_site.register(PartePatron)

#TODO 


