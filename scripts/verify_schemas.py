import sys
from pathlib import Path

from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from health_lakehouse.database.connection import get_engine


def main():
    engine = get_engine()
    query = text("""
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name IN ('bronze', 'silver', 'gold')
        ORDER BY schema_name;
    """)

    with engine.connect() as connection:
        schemas = connection.execute(query).fetchall()

    print("MEDALLION SCHEMA VERIFICATION")
    for schema in schemas:
        print(f"[OK] {schema[0]}")

    if len(schemas) != 3:
        print("WARNING: One or more schemas are missing.")
    else:
        print("All three schemas are available.")


if __name__ == "__main__":
    main()
