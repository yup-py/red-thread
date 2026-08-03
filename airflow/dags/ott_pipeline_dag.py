from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'ott_pipeline_dag',
    default_args=default_args,
    description='End-to-End OTT Pipeline: Ingestion -> dbt Models -> Data Quality Tests',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # 1. Trigger python ingestion scripts
    run_ingestion = BashOperator(
        task_id='run_raw_ingestion',
        bash_command='python /opt/airflow/ingestion/extract_load.py --all',
    )

    # 2. Load/refresh dbt seed mapping tables (genre & rating standardization)
    dbt_seed = BashOperator(
        task_id='dbt_seed',
        bash_command='cd /opt/airflow/dbt && dbt seed --profiles-dir .',
    )

    # 3. Run dbt transformation models
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt && dbt run --profiles-dir .',
    )

    # 4. Run dbt test suite
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dbt && dbt test --profiles-dir .',
    )

    # Task Execution Flow
    run_ingestion >> dbt_seed >> dbt_run >> dbt_test