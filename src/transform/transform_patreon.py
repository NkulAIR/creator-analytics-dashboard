"""
Transforms raw Patreon API payloads from raw_patreon) table into
revenue_events. Patreon is revenue-side, it never touches content_items or engagement_snapshots.

Patreon's members endpoint gives current pledge state, not
discrete historical charges, so external_transaction_id is
synthesized as member_id:last_charge_date to avoid duplicate rows
across repeated runs on the same billing cycle.

Usage: python -m src.transform.transform_patreon
"""
import os

from sqlalchemy import create_engine, text
from datetime import datetime

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/creator_analytics"
)


def get_platform_account_id(conn, platform_name: str) -> str:
    result = conn.execute(
        text("""
            SELECT pa.id FROM platform_accounts pa
            JOIN platforms p ON p.id = pa.platform_id
            WHERE p.name = :platform_name
            LIMIT 1
        """),
        {"platform_name": platform_name}
    ).fetchone()

    if not result:
        raise ValueError(f"No platform_account found for platform '{platform_name}' — seed it first.")

    return result.id





if __name__ == "__main__":
    n = transform_patreon()
    print(f"Transformed {n} raw records into revenue_events")