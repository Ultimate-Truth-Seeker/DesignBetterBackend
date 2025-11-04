from django.conf import settings as s

print(
    "VARIABLES DE CONFIGURACION\n",
    s.DEBUG, "\n",
    s.FRONTEND_DOMAIN, "\n",
    s.ALLOWED_HOSTS, "\n",
    s.CORS_ALLOWED_ORIGINS, "\n",
    s.CSRF_TRUSTED_ORIGINS, "\n"
)