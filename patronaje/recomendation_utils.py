# apps/core/measures.py
MEASURE_ORDER = ["bust","waist","hip","shoulder","back_length","sleeve"]
MEASURE_UNITS = "cm"  # asegúrate de normalizar a cm antes de vectorizar

# apps/catalog/services/vectorizer.py
def as_float(x):
    if x is None: return None
    try: return float(x)
    except: return None

def build_measure_vector(measures: dict) -> list[float] | None:
    """
    measures: dict con claves como 'bust','waist',... en cm
    Devuelve lista en orden MEASURE_ORDER o None si no hay suficiente señal.
    """
    vec = []
    missing = 0
    for key in MEASURE_ORDER:
        v = as_float(measures.get(key))
        if v is None:
            vec.append(0.0)  # o imputa con media por género si la tienes
            missing += 1
        else:
            vec.append(v)
    # Si faltan demasiadas, podrías devolver None para no indexar
    return vec if missing < len(MEASURE_ORDER) else None

# apps/catalog/services/measure_vectors.py
from django.db import connection

def persist_vector(table: str, id_: int, vec: list[float] | None):
    if vec is None: return
    # pgvector espera literal como '[v1,v2,...]'
    literal = "[" + ",".join(f"{x:.6f}" for x in vec) + "]"
    with connection.cursor() as cur:
        cur.execute(f"UPDATE {table} SET measures_vec = %s WHERE id = %s;", [literal, id_])

def upsert_measurement_table_vec(mt) -> None:
    vec = build_measure_vector(mt.measures or {})
    persist_vector("measurement_table", mt.id, vec)

def upsert_configuration_vec(cfg) -> None:
    if cfg.measurement_source == "table" and cfg.measurement_table:
        measures = cfg.measurement_table.measures or {}
    elif cfg.measurement_source == "custom":
        measures = cfg.custom_measures or {}
    else:
        measures = {}
    vec = build_measure_vector(measures)
    persist_vector("configuration", cfg.id, vec)

# apps/catalog/sql/recommend_templates.sql
SQL = """
WITH q AS (
  SELECT measures_vec AS qvec
  FROM measurement_table
  WHERE id = %(mt_id)s
),
nearest AS (
  SELECT
    c.template_id,
    c.id AS configuration_id,
    (c.measures_vec <-> (SELECT qvec FROM q)) AS dist
  FROM configuration c
  JOIN template t ON t.id = c.template_id
  WHERE c.measures_vec IS NOT NULL
    AND t.status = 'published'
    {category_filter}
  ORDER BY c.measures_vec <-> (SELECT qvec FROM q)
  LIMIT 500
),
agg AS (
  SELECT
    template_id,
    MIN(dist)  AS best_dist,
    AVG(dist)  AS avg_dist,
    COUNT(*)   AS hits
  FROM nearest
  GROUP BY template_id
)
SELECT
  t.id   AS template_id,
  t.code AS template_code,
  t.name AS template_name,
  a.best_dist,
  a.avg_dist,
  a.hits,
  COALESCE(u.approval_rate, 0) AS approval_rate,
  COALESCE(u.popularity, 0)    AS popularity,
  (0.70 * (1.0 / (1.0 + a.best_dist))
   + 0.20 * COALESCE(u.approval_rate, 0)
   + 0.10 * LEAST(COALESCE(u.popularity, 0), 1.0)) AS score
FROM agg a
JOIN template t ON t.id = a.template_id
LEFT JOIN template_usage_stats u ON u.template_id = t.id
ORDER BY score DESC
LIMIT %(top_k)s;
"""

# apps/catalog/sql/nearest_examples.sql
SQL_EXAMPLES = """
WITH q AS (
  SELECT measures_vec AS qvec
  FROM measurement_table
  WHERE id = %(mt_id)s
)
SELECT
  c.id AS configuration_id,
  (c.measures_vec <-> (SELECT qvec FROM q)) AS dist
FROM configuration c
WHERE c.template_id = %(template_id)s
  AND c.measures_vec IS NOT NULL
ORDER BY dist ASC
LIMIT 3;
"""

# apps/catalog/services/recommendations.py

def run_sql(sql: str, params: dict):
    with connection.cursor() as cur:
        cur.execute(sql, params)
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

def recommend_templates(mt_id: int, top_k: int = 12, category: str | None = None):
    # Filtro opcional
    cat_filter = "AND t.category = %(category)s" if category else ""
    from . import recommend_templates_sql as q  # o lee archivo
    sql = q.SQL.format(category_filter=cat_filter)

    rows = run_sql(sql, {"mt_id": mt_id, "top_k": top_k, "category": category})

    # Enriquecimiento con ejemplos
    examples_sql = """
    WITH q AS (SELECT measures_vec AS qvec FROM measurement_table WHERE id = %(mt_id)s)
    SELECT c.id AS configuration_id, (c.measures_vec <-> (SELECT qvec FROM q)) AS dist
    FROM configuration c
    WHERE c.template_id = %(template_id)s AND c.measures_vec IS NOT NULL
    ORDER BY dist ASC LIMIT 3;
    """
    for r in rows:
        ex = run_sql(examples_sql, {"mt_id": mt_id, "template_id": r["template_id"]})
        r["closest_examples"] = ex
        # Puedes calcular deltas si guardas las medidas crudas de esos ejemplos
    return rows