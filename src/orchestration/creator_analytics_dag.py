from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.extract.youtube import YouTubeExtractor
from src.extract.twitch import TwitchExtractor
from src.extract.patreon import PatreonExtractor
from src.load.load_raw import load_raw
from src.transform.transform_youtube import transform_youtube
from src.transform.transform_twitch import transform_twitch
from src.transform.transform_patreon import transform_patreon


def extract_and_load(extractor_cls):
    result = extractor_cls().extract()
    load_raw(result)


with DAG(
    dag_id="creator_analytics_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    extract_youtube = PythonOperator(
        task_id="extract_load_youtube",
        python_callable=extract_and_load,
        op_args=[YouTubeExtractor],
    )
    transform_youtube_task = PythonOperator(
        task_id="transform_youtube",
        python_callable=transform_youtube,
    )

    extract_twitch = PythonOperator(
        task_id="extract_load_twitch",
        python_callable=extract_and_load,
        op_args=[TwitchExtractor],
    )
    transform_twitch_task = PythonOperator(
        task_id="transform_twitch",
        python_callable=transform_twitch,
    )

    extract_patreon = PythonOperator(
        task_id="extract_load_patreon",
        python_callable=extract_and_load,
        op_args=[PatreonExtractor],
    )
    transform_patreon_task = PythonOperator(
        task_id="transform_patreon",
        python_callable=transform_patreon,
    )

    extract_youtube >> transform_youtube_task
    extract_twitch >> transform_twitch_task
    extract_patreon >> transform_patreon_task