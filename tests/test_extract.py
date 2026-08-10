"""
Starter tests for the extract layer. Fill these in as you implement
each extractor -- mock the HTTP calls (e.g. with `responses` or
`unittest.mock`) rather than hitting real APIs in tests.
"""
from datetime import datetime, timezone

from src.extract.base import ExtractResult


def test_extract_result_holds_records():
    result = ExtractResult(
        source="youtube",
        extracted_at=datetime.now(timezone.utc),
        records=[{"video_id": "abc123"}],
    )
    assert result.source == "youtube"
    assert len(result.records) == 1


# TODO once YouTubeExtractor is implemented:
# def test_youtube_extract_returns_expected_shape(mock_youtube_api):
#     ...

# TODO once ShopifyExtractor is implemented:
# def test_shopify_extract_paginates_correctly(mock_shopify_api):
#     ...
