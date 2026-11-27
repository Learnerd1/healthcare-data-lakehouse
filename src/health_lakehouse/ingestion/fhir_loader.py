import hashlib
import json
import uuid
from pathlib import Path

from sqlalchemy import text

from health_lakehouse.database.connection import get_engine

INSERT_RESOURCE = text("""
    INSERT INTO bronze.fhir_resources
        (batch_id, source_system, resource_type, resource_id,
         source_file, resource_json, content_hash)
    VALUES
        (:batch_id, :source_system, :resource_type, :resource_id,
         :source_file, CAST(:resource_json AS JSONB), :content_hash)
""")


def load_fhir_folder(folder, source_system):
    """Load every FHIR bundle file in a folder into bronze.fhir_resources."""
    folder = Path(folder)
    files = sorted(folder.rglob("*.json"))
    engine = get_engine()
    batch_id = str(uuid.uuid4())

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO bronze.ingestion_batches
                    (batch_id, source_name, source_type, source_file)
                VALUES (:b, :s, 'FHIR_BUNDLE', :f)
            """),
            {"b": batch_id, "s": source_system, "f": str(folder)},
        )
        already_loaded = {
            row[0]
            for row in conn.execute(
                text("""
                    SELECT DISTINCT source_file FROM bronze.fhir_resources
                    WHERE source_system = :s
                """),
                {"s": source_system},
            )
        }

    received = loaded = rejected = 0
    error_message = None

    try:
        for path in files:
            if path.name in already_loaded:
                continue

            with open(path, "r", encoding="utf-8") as f:
                bundle = json.load(f)

            rows = []
            for entry in bundle.get("entry", []):
                resource = entry.get("resource")
                received += 1
                if not resource or "resourceType" not in resource:
                    rejected += 1
                    continue
                payload = json.dumps(resource, sort_keys=True)
                rows.append({
                    "batch_id": batch_id,
                    "source_system": source_system,
                    "resource_type": resource["resourceType"],
                    "resource_id": resource.get("id"),
                    "source_file": path.name,
                    "resource_json": payload,
                    "content_hash": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
                })

            if rows:
                with engine.begin() as conn:
                    conn.execute(INSERT_RESOURCE, rows)
                loaded += len(rows)
        status = "COMPLETED"
    except Exception as error:
        status = "FAILED"
        error_message = str(error)

    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE bronze.ingestion_batches
                SET ingestion_status = :st,
                    records_received = :r,
                    records_loaded = :l,
                    records_rejected = :j,
                    completed_at = CURRENT_TIMESTAMP,
                    error_message = :e
                WHERE batch_id = :b
            """),
            {"st": status, "r": received, "l": loaded, "j": rejected,
             "e": error_message, "b": batch_id},
        )

    return {
        "batch_id": batch_id,
        "status": status,
        "files_found": len(files),
        "received": received,
        "loaded": loaded,
        "rejected": rejected,
        "error": error_message,
    }
