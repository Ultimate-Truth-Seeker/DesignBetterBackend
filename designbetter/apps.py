from django.apps import AppConfig


class DesignbetterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'designbetter'
    def ready(self):
        import designbetter.signals  # Asegúrate que este import existe
