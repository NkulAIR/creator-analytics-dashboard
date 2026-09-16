"""
Inserts a platform + platform_account row using an extractor's own
ability to resolve its external account ID 

Usage: python -m src.models.seed
"""
import os

from sqlalchemy import create_engine, text

from src.extract.youtube import YouTubeExtractor
from src.extract.twitch import TwitchExtractor

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/creator_analytics"
)

SEED_SQL = text("""
    INSERT INTO platforms (name, category)
    VALUES (:platform_name, :category)
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO platform_accounts (platform_id, external_account_id, display_name)
    SELECT id, :external_account_id, :display_name
    FROM platforms WHERE name = :platform_name
    ON CONFLICT (platform_id, external_account_id) DO NOTHING;
""")


def seed_platform_account(engine, platform_name: str, category: str,
                           external_account_id: str, display_name: str):
    with engine.begin() as conn:
        conn.execute(SEED_SQL, {
            "platform_name": platform_name,
            "category": category,
            "external_account_id": external_account_id,
            "display_name": display_name,
        })


if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)

    twitch = TwitchExtractor()
    seed_platform_account(
        engine,
        platform_name="twitch",
        category="content",
        external_account_id=twitch.get_broadcaster_id(),
        display_name=twitch.broadcaster_login,
    )
    print("Seeded twitch platform account")