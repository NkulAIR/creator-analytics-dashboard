"""
Airflow DAG stub: extract -> load -> transform, once daily.

Don't wire this up until the manual pipeline (running extract/load/
transform by hand) actually works end to end -- see README build order,
step 6. Automating a broken pipeline just makes it harder to debug.
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def run_extract_and_load(source: str, **_):
    """TODO: import the right extractor + load_raw, call extract() then load_raw()."""
    raise NotImplementedError


def run_transform(**_):
    """TODO: run staging + marts SQL (or `dbt run` if using dbt)."""
    raise NotImplementedError


with DAG(
    dag_id="creator_analytics_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    extract_youtube = PythonOperator(
        task_id="extract_load_youtube",
        python_callable=run_extract_and_load,
        op_kwargs={"source": "youtube"},
    )
    extract_shopify = PythonOperator(
        task_id="extract_load_shopify",
        python_callable=run_extract_and_load,
        op_kwargs={"source": "shopify"},
    )
    transform = PythonOperator(
        task_id="transform",
        python_callable=run_transform,
    )

    [extract_youtube, extract_shopify] >> transform
