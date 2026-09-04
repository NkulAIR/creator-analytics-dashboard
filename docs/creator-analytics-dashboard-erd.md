# Creator Analytics Dashboard — ERD

Core question this schema answers: **which platform drives the most engagement relative to revenue?**

## Design notes

A platform account -->

- `PLATFORM_ACCOUNTS` sits between `PLATFORMS` and everything else, so a single platform (e.g. YouTube) can have multiple connected accounts later if needed.
- `ENGAGEMENT_SNAPSHOTS` stores a new row every time stats are re-pulled for a content item, this preserves history so metrics can be computed over any time window (last 30 days, last quarter, etc.) at query time, rather than baking a fixed window into the schema.
- `REVENUE_EVENTS` is naturally event-shaped, so no snapshotting is needed there.
- Time-window filtering (e.g. "last 30 days") is applied in queries against `captured_at` / `occurred_at`

## Diagram

```mermaid
erDiagram
  PLATFORMS ||--o{ PLATFORM_ACCOUNTS : has
  PLATFORM_ACCOUNTS ||--o{ CONTENT_ITEMS : publishes
  PLATFORM_ACCOUNTS ||--o{ REVENUE_EVENTS : generates
  CONTENT_ITEMS ||--o{ ENGAGEMENT_SNAPSHOTS : tracked_by

  PLATFORMS {
    uuid id PK
    string name
    string category
  }
  PLATFORM_ACCOUNTS {
    uuid id PK
    uuid platform_id FK
    string external_account_id
    string display_name
    timestamp connected_at
  }
  CONTENT_ITEMS {
    uuid id PK
    uuid platform_account_id FK
    string external_content_id
    string title
    timestamp published_at
  }
  ENGAGEMENT_SNAPSHOTS {
    uuid id PK
    uuid content_item_id FK
    timestamp captured_at
    int views
    int likes
    int comments
  }
  REVENUE_EVENTS {
    uuid id PK
    uuid platform_account_id FK
    string external_transaction_id
    decimal amount
    string currency
    timestamp occurred_at
    string event_type
  }
```

## Current platforms

- YouTube
- Twitch
- Shopify
- Patreon

Later additions:
- Kick
- Gumroad
