from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


def check_warehouse():
    hook = PostgresHook(postgres_conn_id="healthcare_warehouse")
    rows = hook.get_records(
        "SELECT current_database(), schema_name "
        "FROM information_schema.schemata "
        "WHERE schema_name IN ('bronze','silver','gold') "
        "ORDER BY schema_name;"
    )
    for row in rows:
        print(row)


with DAG(
    dag_id="test_warehouse_connection",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    PythonOperator(
        task_id="check_warehouse",
        python_callable=check_warehouse,
    )
