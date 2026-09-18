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
        raise ValueError(f"No platform_account found for platform '{platform_name}'")

    return result.id


def insert_revenue_event(conn, platform_account_id: str, external_transaction_id: str,
                          amount: float, occurred_at: datetime) -> None:
    conn.execute(
        text("""
            INSERT INTO revenue_events
                (platform_account_id, external_transaction_id, amount, currency, occurred_at, event_type)
            VALUES
                (:platform_account_id, :external_transaction_id, :amount, 'USD', :occurred_at, 'pledge')
            ON CONFLICT (platform_account_id, external_transaction_id) DO NOTHING
        """),
        {
            "platform_account_id": platform_account_id,
            "external_transaction_id": external_transaction_id,
            "amount": amount,
            "occurred_at": occurred_at,
        }
    )


def transform_patreon(engine=None) -> int:
    engine = engine or create_engine(DATABASE_URL)
    count = 0

    with engine.begin() as conn:
        platform_account_id = get_platform_account_id(conn, "patreon")

        raw_rows = conn.execute(
            text("SELECT extracted_at, payload FROM raw_patreon")
        ).fetchall()

        for row in raw_rows:
            member = row.payload
            attrs = member["attributes"]

            last_charge_date = attrs.get("last_charge_date")
            amount_cents = attrs.get("currently_entitled_amount_cents")

            # Skip patrons with no charge history or zero pledge since
            # theres nothing meaningful to record as revenue.
            if not last_charge_date or not amount_cents:
                continue

            external_transaction_id = f"{member['id']}:{last_charge_date}"
            occurred_at = datetime.fromisoformat(last_charge_date.replace("Z", "+00:00"))

            insert_revenue_event(
                conn,
                platform_account_id=platform_account_id,
                external_transaction_id=external_transaction_id,
                amount=amount_cents / 100,
                occurred_at=occurred_at,
            )
            count += 1

    return count


if __name__ == "__main__":
    n = transform_patreon()
    print(f"Transformed {n} raw records into revenue_events")