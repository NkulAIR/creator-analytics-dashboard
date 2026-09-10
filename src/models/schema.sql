-- Requires gen_random_uuid() for UUID primary keys
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS platforms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS platform_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform_id UUID NOT NULL REFERENCES platforms(id),
    external_account_id TEXT NOT NULL,
    display_name TEXT,
    connected_at TIMESTAMP NOT NULL DEFAULT now(),
    UNIQUE (platform_id, external_account_id)
);

CREATE TABLE IF NOT EXISTS content_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform_account_id UUID NOT NULL REFERENCES platform_accounts(id),
    external_content_id TEXT NOT NULL,
    title TEXT,
    published_at TIMESTAMP,
    UNIQUE (platform_account_id, external_content_id)
);

CREATE TABLE IF NOT EXISTS engagement_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_item_id UUID NOT NULL REFERENCES content_items(id),
    captured_at TIMESTAMP NOT NULL,
    views INTEGER,
    likes INTEGER,
    comments INTEGER
);

CREATE TABLE IF NOT EXISTS revenue_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform_account_id UUID NOT NULL REFERENCES platform_accounts(id),
    external_transaction_id TEXT,
    amount NUMERIC(12, 2) NOT NULL,
    currency TEXT NOT NULL DEFAULT 'USD',
    occurred_at TIMESTAMP NOT NULL,
    event_type TEXT NOT NULL
);