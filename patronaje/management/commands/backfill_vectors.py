# apps/catalog/management/commands/backfill_vectors.py
from django.core.management.base import BaseCommand
from patronaje.models import MeasurementTable, Configuration
from patronaje.recomendation_utils import upsert_configuration_vec, upsert_measurement_table_vec

class Command(BaseCommand):
    help = "Construye vectors pgvector para measurement_table y configuration"

    def handle(self, *args, **opts):
        for mt in MeasurementTable.objects.all().iterator():
            upsert_measurement_table_vec(mt)
        for cfg in Configuration.objects.all().iterator():
            upsert_configuration_vec(cfg)
        self.stdout.write(self.style.SUCCESS("Backfill ok"))