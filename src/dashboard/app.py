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

st.set_page_config(page_title="Creator Analytics Dashboard", layout="wide")
st.title("Creator Analytics Dashboard")
st.caption("Which platform drives the most engagement relative to revenue?")

engine = create_engine(DATABASE_URL)

# --- Core metric: revenue per 1000 views, by platform ---
st.header("Revenue per 1,000 Views (last 30 days)")

rows = get_revenue_per_view(engine)
df = pd.DataFrame(rows, columns=["platform", "views", "revenue", "revenue_per_1000_views"])

col1, col2 = st.columns([2, 1])
with col1:
    st.dataframe(df, use_container_width=True, hide_index=True)
with col2:
    chart_df = df.dropna(subset=["revenue_per_1000_views"]).set_index("platform")
    if not chart_df.empty:
        st.bar_chart(chart_df["revenue_per_1000_views"])
    else:
        st.info("No platforms have both views and revenue data yet.")

st.header("Content Performance (latest snapshot)")

with engine.connect() as conn:
    content_df = pd.read_sql(text(CONTENT_DETAIL_QUERY), conn)

selected_platform = st.selectbox(
    "Filter by platform",
    options=["All"] + sorted(content_df["platform"].unique().tolist()),
)

if selected_platform != "All":
    content_df = content_df[content_df["platform"] == selected_platform]

st.dataframe(content_df, use_container_width=True, hide_index=True)