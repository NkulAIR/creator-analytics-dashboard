"""
Patreon API extractor.

Build this last -- see README build order. Pulls pledges/membership
data (revenue events) from the creator's Patreon campaign.

Auth: OAuth 2.0 creator access token (PATREON_ACCESS_TOKEN).

Docs: https://docs.patreon.com/
"""
from datetime import datetime
import os

from .base import BaseExtractor, ExtractResult


class PatreonExtractor(BaseExtractor):
    source_name = "patreon"

    def __init__(self, access_token: str | None = None):
        self.access_token = access_token or os.environ["PATREON_ACCESS_TOKEN"]

    def extract(self, since: datetime | None = None) -> ExtractResult:
        """
        TODO:
        1. GET /api/oauth2/v2/campaigns/{campaign_id}/members
        2. Include fields for pledge amount, status, last_charge_date
        3. Return raw member/pledge records as-is -- don't transform here
        """
        raise NotImplementedError("Implement Patreon API calls here")


if __name__ == "__main__":
    extractor = PatreonExtractor()
    result = extractor.extract()
    print(f"Pulled {len(result.records)} records from {result.source}")
