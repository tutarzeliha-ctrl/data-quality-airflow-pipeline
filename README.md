🚀 Production-Grade Medallion Data Pipeline with Airflow, Polars, & DuckDB
This project delivers a production-grade data pipeline designed to stand out in data engineering portfolios and interviews. Moving beyond generic Kaggle-style scripts, it combines modern technologies, data quality automation, and a robust Medallion Architecture (Bronze -> Silver -> Gold).

🏗️ Executive Summary
Project Goal: Process 1 million rows of transactional data with high performance, catch data quality anomalies early, and deliver reliable analytical reports for business units.

💡 Automated Orchestration: Fully managed via Apache Airflow.

⚡ High-Performance Processing: Built with Polars (Rust-backed) for up to 10x faster data transformation compared to Pandas.

🛡️ Data Quality Gates: Automated assertion rules to prevent dirty or invalid data from reaching downstream analytics.

📈 SQL-First Analytics: Powered by DuckDB for lightning-fast SQL querying over processed Parquet files.

🗺️ Pipeline Architecture & Data Flow
Kod snippet'i
graph LR
    subgraph "Source"
        A[raw_sales.csv <br/> 1 Million Rows]
    end

    subgraph "Airflow Pipeline"
        B[Bronze Ingestion] -->|Polars Cleaning| C[Silver Layer .parquet]
        C -->|Data Quality Gates| D{Assertion Check}
        D -->|Passed| E[Gold Layer Aggregation]
        D -->|Failed| F[Task Failure & Alert]
    end

    subgraph "Serving"
        E -->|DuckDB SQL| G[store_performance.csv]
    end

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#bbf,stroke:#333,stroke-width:2px
    style E fill:#bfb,stroke:#333,stroke-width:2px
    style D fill:#f96,stroke:#333,stroke-width:4px


🛠️ Production-Grade Tech Stack
Component               Tool Selection    Production Benefit                                                              Orchestration           Apache Airflow    Automated retries, DAG visualization, and robust scheduling.
Transformation          Polars & DuckDB   Blazing fast speed, memory efficiency, and native SQL capabilities.
Storage Format          Apache Parquet    Columnar compression and highly efficient analytical scans.
Quality Control         Custom Assertions Enforced data contracts and automated task failure on data errors.


⚙️ Quick Start (Local Docker Setup)
To run this project locally, execute the following commands in your terminal:

Clone the repository:

Bash
git clone https://github.com/tutarzeliha-ctrl/data-quality-airflow-pipeline.git
cd data-quality-airflow-pipeline
Spin up Airflow using Docker Compose:

Bash
docker compose up --build -d
Generate 1 Million rows of synthetic test data:

Bash
python generate_data.py
Open the Airflow UI at http://localhost:8081 and trigger the DAG!
