"""
Minimal Streamlit dashboard reading from the unified marts.

Run with: streamlit run src/dashboard/app.py
"""
import os

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/creator_analytics"
)

st.set_page_config(page_title="Creator Analytics", layout="wide")
st.title("Creator analytics")

engine = create_engine(DATABASE_URL)

st.header("Revenue over time")
revenue_df = pd.read_sql("SELECT event_date, source, amount FROM revenue_event", engine)
if not revenue_df.empty:
    fig = px.bar(revenue_df, x="event_date", y="amount", color="source", barmode="stack")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No revenue data yet -- run the extract/load/transform pipeline first.")

st.header("Engagement over time")
engagement_df = pd.read_sql(
    "SELECT event_date, metric_name, metric_value FROM engagement_event", engine
)
if not engagement_df.empty:
    fig2 = px.line(engagement_df, x="event_date", y="metric_value", color="metric_name")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No engagement data yet -- run the extract/load/transform pipeline first.")
