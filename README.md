# Production-Grade Medallion Data Pipeline 🚀

An end-to-end, high-performance Data Engineering pipeline built with **Apache Airflow**, **Polars**, and **DuckDB**, implementing the **Medallion Architecture (Bronze -> Silver -> Gold)** with automated **Data Quality Gates**.

---

## 🏗️ Architecture & Tech Stack

* **Orchestration:** Apache Airflow (Dockerized)
* **Processing Engine:** Polars (Rust-backed, 10x faster than Pandas)
* **Analytical SQL Engine:** DuckDB
* **Data Quality:** Automated assertion gates (Null checks, row count & value validations)
* **Storage Format:** Apache Parquet (Columnar compression)

---

## 🔄 Data Pipeline Flow

1. **Bronze Layer (`raw_sales.csv`):** Ingestion of raw, untransformed transactional data containing deliberate data quality issues (nulls, missing values).
2. **Silver Layer (`clean_sales.parquet`):** Polars reads 1M+ rows in parallel, cleans invalid records, and optimizes storage into Parquet format.
3. **Data Quality Gate:** Automated validation checks ensuring zero null values and no negative transaction amounts before analytics execution.
4. **Gold Layer (`store_performance.csv`):** DuckDB runs high-performance analytical SQL queries over the Parquet files to produce business-ready KPIs (e.g., store performance, total sales, transaction counts).

---

## ⚙️ Quick Start (Local Docker Setup)

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/data-quality-airflow-pipeline.git](https://github.com/your-username/data-quality-airflow-pipeline.git)
   cd data-quality-airflow-pipeline