"""
Loads ExtractResult records into raw warehouse tables, untouched.

Keep this dumb on purpose: one raw table per source (raw_youtube,
raw_shopify, raw_patreon), each storing the full JSON payload plus
minimal metadata. All reconciliation happens later in src/models/.
This way a schema change upstream never breaks the load step --
only the transform step needs updating.
"""
import json
import os

from sqlalchemy import create_engine, text

from src.extract.base import ExtractResult

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/creator_analytics"
)

RAW_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS raw_{source} (
    id SERIAL PRIMARY KEY,
    extracted_at TIMESTAMP NOT NULL,
    payload JSONB NOT NULL
);
"""


def ensure_raw_table(engine, source: str) -> None:
    with engine.begin() as conn:
        conn.execute(text(RAW_TABLE_DDL.format(source=source)))


def load_raw(result: ExtractResult, engine=None) -> int:
    """Writes every record in an ExtractResult to its raw table.
    Returns the number of rows written."""
    engine = engine or create_engine(DATABASE_URL)
    ensure_raw_table(engine, result.source)

    insert_sql = text(
        f"INSERT INTO raw_{result.source} (extracted_at, payload) VALUES (:extracted_at, :payload)"
    )
    with engine.begin() as conn:
        for record in result.records:
            conn.execute(
                insert_sql,
                {"extracted_at": result.extracted_at, "payload": json.dumps(record)},
            )
    return len(result.records)


if __name__ == "__main__":
    # Example: python -m src.load.load_raw
    from datetime import datetime, timezone
    from src.extract.base import ExtractResult

    dummy = ExtractResult(
        source="youtube", extracted_at=datetime.now(timezone.utc), records=[{"video_id": "abc123"}]
    )
    n = load_raw(dummy)
    print(f"Loaded {n} rows into raw_{dummy.source}")
