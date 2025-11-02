# backend_django/settings_production.py
from decouple import config, Csv
from .settings import *  # ← Hereda TODO tu settings.py

# === PRODUCCIÓN: SOBREESCRIBE LO NECESARIO ===

# 1. DEBUG
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

# 2. SECRET_KEY
SECRET_KEY = config('DJANGO_SECRET_KEY')

# 3. ALLOWED_HOSTS
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', cast=Csv())

# 4. Seguridad SSL
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 5. Base de datos (producción)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# 6. CORS (producción)
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOWED_CREDENTIALS = True

# 7. Static files (para collectstatic)
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# 8. Media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 9. Email (usa variables de .env)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# 10. Social Auth (usa .env)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_FACEBOOK_KEY = config('FACEBOOK_OAUTH2_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = config('FACEBOOK_OAUTH2_SECRET')

# 11. Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'WARNING',
    },
}