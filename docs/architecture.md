# Architecture

```
YouTube API   ┐
Shopify API   ├──> Extract ──> Load (raw tables) ──> Transform (marts) ──> Serve (dashboard)
Patreon API   ┘
```

- **Extract**: one module per platform (`src/extract/`), each pulling raw
  records via that platform's API. Incremental where the API supports it
  (e.g. `updated_at_min` on Shopify).
- **Load**: raw records are written untouched into `raw_<source>` tables
  as JSONB (`src/load/load_raw.py`). Nothing is reshaped here -- the goal
  is a durable, replayable copy of what the API returned.
- **Transform**: `src/models/staging/` cleans and types raw JSON into flat
  tables. `src/models/marts/` reconciles the three different shapes
  (a video, an order, a pledge) into two unified fact tables:
  `revenue_event` and `engagement_event`.
- **Serve**: `src/dashboard/app.py` (Streamlit) queries the marts directly.
- **Orchestration**: `src/orchestration/dags/` schedules extract -> load ->
  transform to run daily once the manual pipeline works end to end.

See `erd.md` for the data model these stages produce.
