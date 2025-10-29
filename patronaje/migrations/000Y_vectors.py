# apps/catalog/migrations/000Y_vectors.py
from django.db import migrations

OPS = [
"""
ALTER TABLE patronaje_measurementtable
    ADD COLUMN IF NOT EXISTS measures_vec vector(6);
""",
"""
ALTER TABLE patronaje_configuration
    ADD COLUMN IF NOT EXISTS measures_vec vector(6);
""",
# índices ivfflat
"""
CREATE INDEX IF NOT EXISTS idx_measurement_table_vec
ON patronaje_measurementtable USING ivfflat (measures_vec vector_l2_ops) WITH (lists = 100);
""",
"""
CREATE INDEX IF NOT EXISTS idx_configuration_vec
ON patronaje_configuration USING ivfflat (measures_vec vector_l2_ops) WITH (lists = 100);
"""
]

def forwards(apps, schema_editor):
    with schema_editor.connection.cursor() as cur:
        for sql in OPS: cur.execute(sql)

class Migration(migrations.Migration):
    dependencies = [("patronaje","000X_pgvector")]
    operations = [migrations.RunPython(forwards)]