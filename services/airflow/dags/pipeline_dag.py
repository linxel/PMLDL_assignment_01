from airflow import DAG
from datetime import datetime

from airflow.providers.standard.operators.bash import BashOperator

with DAG(
    'mlops_pipeline',
    schedule='*/5 * * * *',  # Every 5 minutes
    start_date=datetime(2026, 1, 1),
    catchup=False
) as dag:

    data_task = BashOperator(
        task_id='data_engineering',
        bash_command='python code/datasets/data_engineering.py'
    )

    model_task = BashOperator(
        task_id='model_engineering',
        bash_command='python code/models/model_engineering.py'
    )

    deploy_task = BashOperator(
        task_id='deployment',
        bash_command='cd code/deployment && docker compose up -d'
    )

    data_task >> model_task >> deploy_task
