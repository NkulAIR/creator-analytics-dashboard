"""
Analytics queries answering the dashboard's core question:
which platform drives the most engagement relative to revenue.
"""
import os

from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/creator_analytics"
)

REVENUE_PER_VIEW_QUERY = """
WITH latest_snapshots AS (
    SELECT DISTINCT ON (content_item_id) content_item_id, views, captured_at
    FROM engagement_snapshots
    WHERE captured_at >= now() - interval '30 days'
    ORDER BY content_item_id, captured_at DESC
),
platform_engagement AS (
    SELECT pa.platform_id, SUM(ls.views) AS total_views
    FROM latest_snapshots ls
    JOIN content_items ci ON ci.id = ls.content_item_id
    JOIN platform_accounts pa ON pa.id = ci.platform_account_id
    GROUP BY pa.platform_id
),
platform_revenue AS (
    SELECT pa.platform_id, SUM(re.amount) AS total_revenue
    FROM revenue_events re
    JOIN platform_accounts pa ON pa.id = re.platform_account_id
    WHERE re.occurred_at >= now() - interval '30 days'
    GROUP BY pa.platform_id
)
SELECT
    p.name AS platform,
    COALESCE(pe.total_views, 0) AS views,
    COALESCE(pr.total_revenue, 0) AS revenue,
    CASE
        WHEN COALESCE(pe.total_views, 0) = 0 THEN NULL
        ELSE ROUND((COALESCE(pr.total_revenue, 0) / pe.total_views) * 1000, 2)
    END AS revenue_per_1000_views
FROM platforms p
LEFT JOIN platform_engagement pe ON pe.platform_id = p.id
LEFT JOIN platform_revenue pr ON pr.platform_id = p.id
ORDER BY revenue_per_1000_views DESC NULLS LAST;
"""


def get_revenue_per_view(engine=None):
    engine = engine or create_engine(DATABASE_URL)

    with engine.connect() as conn:
        result = conn.execute(text(REVENUE_PER_VIEW_QUERY))
        return result.fetchall()


if __name__ == "__main__":
    rows = get_revenue_per_view()
    for row in rows:
        print(f"{row.platform}: {row.views} views, R{row.revenue} revenue, "
              f"R{row.revenue_per_1000_views}/1000 views")