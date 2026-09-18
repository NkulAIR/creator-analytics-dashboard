"""
Streamlit dashboard for the Creator Analytics Unification project.

Usage: streamlit run src/dashboard/app.py
"""
import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

from src.analytics.queries import get_revenue_per_view

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/creator_analytics"
)

CONTENT_DETAIL_QUERY = """
SELECT
    p.name AS platform,
    ci.title,
    ci.published_at,
    es.views,
    es.likes,
    es.comments,
    es.captured_at
FROM content_items ci
JOIN platform_accounts pa ON pa.id = ci.platform_account_id
JOIN platforms p ON p.id = pa.platform_id
JOIN LATERAL (
    SELECT views, likes, comments, captured_at
    FROM engagement_snapshots
    WHERE content_item_id = ci.id
    ORDER BY captured_at DESC
    LIMIT 1
) es ON true
ORDER BY es.views DESC;
"""