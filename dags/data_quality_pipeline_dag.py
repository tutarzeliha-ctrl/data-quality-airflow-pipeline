from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import polars as pl
import duckdb
import os

default_args = {
    'owner': 'zeliha',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def process_bronze_to_silver():
    """Reads 1M rows, cleans nulls, and saves as Parquet (Silver Layer)."""
    raw_path = '/opt/airflow/data/raw_sales.csv'
    silver_dir = '/opt/airflow/data/silver'
    os.makedirs(silver_dir, exist_ok=True)
    silver_path = os.path.join(silver_dir, 'clean_sales.parquet')

    print("Reading 1M rows with Polars...")
    df = pl.read_csv(raw_path, infer_schema_length=10000)
    
    # Data Quality Gate: Filter out null amounts
    df_clean = df.filter(pl.col('amount').is_not_null())
    df_clean.write_parquet(silver_path)
    print(f"Silver Layer created: {silver_path}")

def run_data_quality_checks():
    """
    Data Quality Validation (Great Expectations style logic):
    Ensures that the cleaned dataset meets structural and business constraints.
    """
    silver_path = '/opt/airflow/data/silver/clean_sales.parquet'
    df = pl.read_parquet(silver_path)

    print("Running Data Quality Assertions...")

    # Rule 1: Dataset must not be empty
    assert len(df) > 0, "Data Quality Error: Dataset is empty!"

    # Rule 2: There should be zero null amounts remaining after Silver layer
    null_count = df.filter(pl.col('amount').is_null()).height
    assert null_count == 0, f"Data Quality Error: Found {null_count} null amounts in Silver layer!"

    # Rule 3: All transaction amounts must be greater than zero (no negative sales)
    min_amount = df.select(pl.min('amount')).item()
    assert min_amount > 0, f"Data Quality Error: Invalid negative or zero amount found: {min_amount}"

    print("All Data Quality Checks Passed Successfully! ✅")

def process_silver_to_gold():
    """Aggregates clean data using DuckDB (Gold Layer)."""
    silver_path = '/opt/airflow/data/silver/clean_sales.parquet'
    gold_dir = '/opt/airflow/data/gold'
    os.makedirs(gold_dir, exist_ok=True)
    gold_path = os.path.join(gold_dir, 'store_performance.csv')

    conn = duckdb.connect()
    query = f"""
        SELECT 
            store_location, 
            ROUND(SUM(amount), 2) as total_sales,
            COUNT(transaction_id) as total_transactions,
            ROUND(AVG(amount), 2) as avg_order_value
        FROM read_parquet('{silver_path}')
        GROUP BY store_location
        ORDER BY total_sales DESC
    """
    
    df_gold = conn.execute(query).pl()
    print("--- Gold Layer: Store Performance Report ---")
    print(df_gold)
    
    df_gold.write_csv(gold_path)
    print(f"Gold Layer report saved to: {gold_path}")

with DAG(
    'data_quality_pipeline',
    default_args=default_args,
    description='Production Medallion Pipeline with Data Quality Gates',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['medallion', 'polars', 'duckdb', 'data-quality'],
) as dag:

    task_silver = PythonOperator(
        task_id='process_bronze_to_silver_task',
        python_callable=process_bronze_to_silver,
    )

    task_quality_check = PythonOperator(
        task_id='run_data_quality_checks_task',
        python_callable=run_data_quality_checks,
    )

    task_gold = PythonOperator(
        task_id='aggregate_data_gold_task',
        python_callable=process_silver_to_gold,
    )

    # Pipeline Flow: Silver -> Quality Gate -> Gold
    task_silver >> task_quality_check >> task_gold