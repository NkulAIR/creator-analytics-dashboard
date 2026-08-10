"""
Shopify Admin API extractor.

Pulls orders (revenue events). Add products/customers later if the
dashboard needs them.

Auth: private app access token (SHOPIFY_ACCESS_TOKEN) scoped to
read_orders. Shopify paginates via Link headers (cursor-based) --
don't try to use page numbers, they're deprecated.

Docs: https://shopify.dev/docs/api/admin-rest
"""
from datetime import datetime
import os

from .base import BaseExtractor, ExtractResult


class ShopifyExtractor(BaseExtractor):
    source_name = "shopify"

    def __init__(self, store_name: str | None = None, access_token: str | None = None):
        self.store_name = store_name or os.environ["SHOPIFY_STORE_NAME"]
        self.access_token = access_token or os.environ["SHOPIFY_ACCESS_TOKEN"]
        self.base_url = f"https://{self.store_name}.myshopify.com/admin/api/2024-07"

    def extract(self, since: datetime | None = None) -> ExtractResult:
        """
        TODO:
        1. GET {base_url}/orders.json?status=any&updated_at_min={since}
        2. Follow the Link header for cursor-based pagination
        3. Return raw order records as-is -- don't transform here
        """
        raise NotImplementedError("Implement Shopify API calls here")


if __name__ == "__main__":
    extractor = ShopifyExtractor()
    result = extractor.extract()
    print(f"Pulled {len(result.records)} records from {result.source}")
