from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

PROJECT = Path("/opt/project")


def load_bronze():
    from health_lakehouse.ingestion.fhir_loader import load_fhir_folder

    result = load_fhir_folder(
        PROJECT / "data" / "raw" / "synthea",
        source_system="synthea_r4_100",
    )
    print(result)
    if result["status"] != "COMPLETED":
        raise RuntimeError(result["error"])


def run_sql_file(relative_path):
    sql = (PROJECT / relative_path).read_text()
    PostgresHook(postgres_conn_id="healthcare_warehouse").run(sql)


with DAG(
    dag_id="lakehouse_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    bronze = PythonOperator(task_id="load_bronze", python_callable=load_bronze)
    silver = PythonOperator(
        task_id="build_silver",
        python_callable=run_sql_file,
        op_args=["sql/silver/create_silver.sql"],
    )
    gold = PythonOperator(
        task_id="build_gold",
        python_callable=run_sql_file,
        op_args=["sql/gold/create_gold.sql"],
    )

    bronze >> silver >> gold
