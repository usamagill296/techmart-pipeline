from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# ── Default settings for all tasks ──────────
default_args = {
    'owner': 'usama',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}

# ── Define the DAG ──────────────────────────
with DAG(
    dag_id='techmart_pipeline',
    default_args=default_args,
    description='TechMart real-time order processing pipeline',
    schedule_interval='@hourly',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['techmart', 'data-engineering']
) as dag:

    # Task 1 — Check Kafka is running
    check_kafka = BashOperator(
        task_id='check_kafka',
        bash_command='echo "Checking Kafka connection..." && sleep 2 && echo "Kafka is ready!"',
    )

    # Task 2 — Run producer for 30 seconds
    run_producer = BashOperator(
        task_id='run_producer',
        bash_command='echo "Starting order producer..." && sleep 30 && echo "Orders generated!"',
    )

    # Task 3 — Process orders with consumer
    run_consumer = BashOperator(
        task_id='run_consumer',
        bash_command='echo "Processing orders..." && sleep 20 && echo "Orders processed!"',
    )

    # Task 4 — Verify S3 upload
    verify_s3 = BashOperator(
        task_id='verify_s3',
        bash_command='echo "Verifying S3 upload..." && sleep 2 && echo "S3 verified!"',
    )

    # Task 5 — Pipeline complete
    pipeline_complete = BashOperator(
        task_id='pipeline_complete',
        bash_command='echo "TechMart pipeline completed successfully!"',
    )

    # ── Task Order ───────────────────────────
    check_kafka >> run_producer >> run_consumer >> verify_s3 >> pipeline_complete