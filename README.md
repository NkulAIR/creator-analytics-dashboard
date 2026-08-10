# Creator Analytics Unification Dashboard

A data engineering project that unifies a content creator's siloed data —
YouTube, Shopify, and Patreon — into a single warehouse and dashboard, so
overall business growth can be analyzed in one place instead of across
three disconnected platforms.

## Problem

Creator data lives in silos: audience/engagement data on YouTube, product
sales on Shopify, membership revenue on Patreon. There's no single place
to answer questions like "does posting more videos actually grow revenue?"

## Architecture

Extract → Load → Transform → Serve, coordinated by an orchestrator.

- **Extract**: pull raw data from each platform's API (incremental where
  possible)
- **Load**: land raw JSON/records into warehouse tables, untouched
- **Transform**: reconcile source-specific shapes into a unified model
  (`revenue_event`, `engagement_event`) via dbt or plain SQL
- **Serve**: a dashboard (Streamlit) queries the unified model

See `docs/architecture.md` and `docs/erd.md` for diagrams.

## Getting started

```bash
cp .env.example .env        # fill in API credentials
docker-compose up -d        # starts local Postgres
pip install -r requirements.txt
```


## Project layout

```
src/
  extract/         # one module per source platform
  load/             # writes extracted data into raw warehouse tables
  models/
    staging/        # 1:1 cleaned versions of raw tables
    marts/          # unified revenue_event / engagement_event models
  orchestration/    # DAGs / flows scheduling extract -> load -> transform
  dashboard/        # Streamlit app querying the marts
tests/
docs/
```
## Verification Code

WTC-7DQEH5VQ
