"""
Starter tests for the transform layer. Once staging/marts SQL is wired
into a query runner, test that reconciliation logic is correct --
e.g. only 'paid' Shopify orders and 'active_patron' Patreon members
should appear in revenue_event.
"""
import pytest


@pytest.mark.skip(reason="Wire up a test DB / query runner first")
def test_revenue_event_excludes_unpaid_shopify_orders():
    ...


@pytest.mark.skip(reason="Wire up a test DB / query runner first")
def test_revenue_event_excludes_declined_patreon_pledges():
    ...
