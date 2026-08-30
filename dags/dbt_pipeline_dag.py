# Airflow DAG to automate dbt run and test tasks
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'zeliha',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dbt_sales_pipeline',
    default_args=default_args,
    description='Run dbt models for sales data quality pipeline',
    schedule_interval='@daily',
    start_date=datetime(2026, 8, 29),
    catchup=False,
) as dag:

    # Run dbt models inside the transform_project directory
    run_dbt = BashOperator(
        task_id='dbt_run_models',
        bash_command='cd /opt/airflow/transform_project && dbt run --no-partial-parse',
    )

    # Run dbt tests to ensure data quality
    test_dbt = BashOperator(
        task_id='dbt_test_models',
        bash_command='cd /opt/airflow/transform_project && dbt test',
    )

    run_dbt >> test_dbt