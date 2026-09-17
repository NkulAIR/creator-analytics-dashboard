"""
Patreon API v2 extractor.

A revenue side extractor which pulls campaign membership/pledge data and its output feeds
revenue_events, not content_items/engagement_snapshots.

Auth: OAuth 2.0 (authorization code flow via patreon_auth.py).

"""
from datetime import datetime, timezone
import os

import requests
from dotenv import load_dotenv

from .base import BaseExtractor, ExtractResult
from .helpers.patreon_auth import get_patreon_access_token

load_dotenv()

BASE_URL = "https://www.patreon.com/api/oauth2/v2"