#migrations/000X_pgvector.py
from django.db import migrations

SQL_ENABLE = "CREATE EXTENSION IF NOT EXISTS vector;"

def enable_pgvector(apps, schema_editor):
    with schema_editor.connection.cursor() as cur:
        cur.execute(SQL_ENABLE)

class Migration(migrations.Migration):
    dependencies = [("patronaje","0001_initial")]
    operations = [migrations.RunPython(enable_pgvector)]