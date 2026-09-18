"""
Streamlit dashboard for the Creator Analytics Unification project.

Usage: streamlit run src/dashboard/app.py
"""
import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/creator_analytics"
)