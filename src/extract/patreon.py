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

class PatreonExtractor(BaseExtractor):
    source_name = "patreon"

    def __init__(self):
        self.access_token = get_patreon_access_token()
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            # Patreon returns a 403 which could look like an auth error
            # if this header is missing entirely.
            "User-Agent": "creator-analytics-dashboard (personal project)",
        }

    def _get_campaign_id(self) -> str:
        response = requests.get(
            f"{BASE_URL}/campaigns",
            headers=self.headers,
        )
        response.raise_for_status()
        data = response.json()["data"]

        if not data:
            raise ValueError("No Patreon campaign found for this account.")

        return data[0]["id"]