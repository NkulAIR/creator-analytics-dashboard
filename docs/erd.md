# Data model

The unified marts layer, expressed as an ER diagram (view with any
mermaid-compatible renderer, e.g. GitHub or the mermaid live editor).

```mermaid
erDiagram
  CREATOR ||--o{ REVENUE_EVENT : earns
  CREATOR ||--o{ ENGAGEMENT_EVENT : generates
  SOURCE ||--o{ REVENUE_EVENT : produces
  SOURCE ||--o{ ENGAGEMENT_EVENT : produces
  DATE_DIM ||--o{ REVENUE_EVENT : occurs_on
  DATE_DIM ||--o{ ENGAGEMENT_EVENT : occurs_on

  CREATOR {
    uuid id PK
    string name
  }
  SOURCE {
    uuid id PK
    string platform
  }
  REVENUE_EVENT {
    uuid id PK
    uuid creator_id FK
    uuid source_id FK
    date event_date FK
    decimal amount
    string type
  }
  ENGAGEMENT_EVENT {
    uuid id PK
    uuid creator_id FK
    uuid source_id FK
    date event_date FK
    string metric_name
    int metric_value
  }
  DATE_DIM {
    date event_date PK
  }
```

## Why two fact tables instead of one

A YouTube view and a Shopify sale don't share attributes -- forcing them
into one giant table means lots of null columns and awkward filtering.
Two fact tables (`revenue_event`, `engagement_event`) keep each shape
clean, while `source` on both makes it possible to trace any row back to
the platform it came from, and to add a new source later without
changing the shape of existing ones.
