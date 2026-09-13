from datetime import datetime, timedelta
from pathlib import Path
import sys
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

BASE_DIR = Path(__file__).resolve().parents[3]
PYTHON_EXEC = sys.executable

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="mlops_automated_pipeline",
    default_args=default_args,
    description="E2E Pipeline: Data Eng -> Model Eng -> Docker Compose Deployment",
    schedule="*/5 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
) as dag:

    stage_1_data_engineering = BashOperator(
        task_id="data_engineering",
        bash_command=f'"{PYTHON_EXEC}" "{BASE_DIR}/code/datasets/data_engineering.py"',
    )

    stage_2_model_engineering = BashOperator(
        task_id="model_engineering",
        bash_command=f'"{PYTHON_EXEC}" "{BASE_DIR}/code/models/model_engineering.py"',
    )

    stage_3_deployment = BashOperator(
        task_id="deployment",
        bash_command=(
            f'docker compose --project-directory "{BASE_DIR}/code/deployment" '
            f'-f "{BASE_DIR}/code/deployment/docker-compose.yml" up -d --build --force-recreate'
        ),
    )

    stage_1_data_engineering >> stage_2_model_engineering >> stage_3_deployment
