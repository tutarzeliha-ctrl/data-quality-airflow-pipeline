# Medallion Pipeline with Airflow, Polars and DuckDB

A local Airflow pipeline that moves synthetic sales data through bronze, silver
and gold layers, with assertion-based data quality checks between the layers.

## What it does

1. **Bronze:** `generate_data.py` writes 1 million synthetic sales rows to
   `data/raw_sales.csv`. About 5% of the `amount` values are left empty on purpose.
2. **Silver:** Polars reads the CSV, drops rows with an empty `amount` and writes
   `data/silver/clean_sales.parquet`.
3. **Quality checks:** the DAG stops if the silver data is empty, still has null
   amounts, or has an amount of zero or less.
4. **Gold:** DuckDB aggregates the silver Parquet file into
   `data/gold/store_performance.csv` (total sales, transactions and average order
   value per store).

An optional Slack callback sends a message when a task fails, if
`SLACK_WEBHOOK_URL` is set.

## Tech stack

| Part | Tool |
| :--- | :--- |
| Orchestration | Apache Airflow (Docker Compose) |
| Transformation | Polars |
| Storage | CSV (bronze), Parquet (silver), CSV (gold) |
| Analytical query | DuckDB |
| Quality checks | Python assertions inside an Airflow task |

The repository also contains a small dbt project (`transform_project/`) and a
second DAG (`dags/dbt_pipeline_dag.py`) that I used to try dbt with DuckDB.

## Run it locally

```bash
git clone https://github.com/tutarzeliha-ctrl/data-quality-airflow-pipeline.git
cd data-quality-airflow-pipeline
mkdir data
python generate_data.py
docker compose up --build -d
```

Then open the Airflow UI at http://localhost:8081 and trigger the
`data_quality_pipeline` DAG.

## Limitations

- Synthetic data only.
- The null-amount check runs after the silver step has already removed nulls,
  so it can only fail if that step changes. A stronger version would count and
  report the removed rows.
- Performance was not benchmarked; there is no comparison with Pandas.
- The Slack alert has not been tested against a live workspace.
- Generated data and Airflow logs are not stored in the repository; create them
  with the steps above.