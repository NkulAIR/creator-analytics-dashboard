# reads from the raw_youtube table
# looks up platform_account_id
# populates content_items + engagement_snapshots using the upsert pattern.

"""
Transforms raw YouTube API payloads (from raw_youtube) into the
content_items and engagement_snapshots tables.

Usage: python -m src.transform.transform_youtube
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


def upsert_content_item(conn, platform_account_id: str, external_content_id: str,
                         title: str, published_at: datetime) -> str:
    inserted = conn.execute(
        text("""
            INSERT INTO content_items (platform_account_id, external_content_id, title, published_at)
            VALUES (:platform_account_id, :external_content_id, :title, :published_at)
            ON CONFLICT (platform_account_id, external_content_id) DO NOTHING
            RETURNING id
        """),
        {
            "platform_account_id": platform_account_id,
            "external_content_id": external_content_id,
            "title": title,
            "published_at": published_at,
        }
    ).fetchone()

    if inserted:
        return inserted.id

    existing = conn.execute(
        text("""
            SELECT id FROM content_items
            WHERE platform_account_id = :platform_account_id
            AND external_content_id = :external_content_id
        """),
        {"platform_account_id": platform_account_id, "external_content_id": external_content_id}
    ).fetchone()

    return existing.id


def insert_engagement_snapshot(conn, content_item_id: str, captured_at: datetime,
                                views: int, likes: int, comments: int) -> None:
    conn.execute(
        text("""
            INSERT INTO engagement_snapshots (content_item_id, captured_at, views, likes, comments)
            VALUES (:content_item_id, :captured_at, :views, :likes, :comments)
        """),
        {
            "content_item_id": content_item_id,
            "captured_at": captured_at,
            "views": views,
            "likes": likes,
            "comments": comments,
        }
    )

def transform_youtube(engine=None) -> int:
    engine = engine or create_engine(DATABASE_URL)
    count = 0

    with engine.begin() as conn:
        platform_account_id = get_platform_account_id(conn, "youtube")

        raw_rows = conn.execute(
            text("SELECT extracted_at, payload FROM raw_youtube")
        ).fetchall()

        for row in raw_rows:
            payload = row.payload
            published_at = datetime.fromisoformat(
                payload["snippet"]["publishedAt"].replace("Z", "+00:00")
            )

            content_item_id = upsert_content_item(
                conn,
                platform_account_id=platform_account_id,
                external_content_id=payload["id"],
                title=payload["snippet"]["title"],
                published_at=published_at,
            )

            insert_engagement_snapshot(
                conn,
                content_item_id=content_item_id,
                captured_at=row.extracted_at,
                views=int(payload["statistics"].get("viewCount", 0)),
                likes=int(payload["statistics"].get("likeCount", 0)),
                comments=int(payload["statistics"].get("commentCount", 0)),
            )
            count += 1

    return count


if __name__ == "__main__":
    n = transform_youtube()
    print(f"Transformed {n} raw records into content_items/engagement_snapshots")