"""
Apache Airflow DAG for Weather Prediction Pipeline
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import sys
from pathlib import Path

# Add project root to path
# In Docker, the project is mounted at /opt/airflow
# The src directory is mounted at /opt/airflow/src
import os
if os.path.exists('/opt/airflow/src'):
    # Running in Docker
    sys.path.insert(0, '/opt/airflow')
else:
    # Running locally
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from src.data.extract import extract_weather_data
from src.data.transform import transform_weather_data

default_args = {
    'owner': 'mlops-team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weather_prediction_pipeline',
    default_args=default_args,
    description='MLOps pipeline for weather prediction',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    tags=['mlops', 'weather', 'prediction'],
)

extract_task = PythonOperator(
    task_id='extract_weather_data',
    python_callable=extract_weather_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_weather_data',
    python_callable=transform_weather_data,
    dag=dag,
)

# Update dependencies
extract_task >> transform_task

