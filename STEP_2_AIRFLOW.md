# Step 2: Apache Airflow Setup and DAG Creation

## 👤 Assigned to: Member 1

## Objective
Install and configure Apache Airflow, then create DAGs for data extraction, transformation, and loading.

## Prerequisites
- Step 1 completed
- Python 3.8+ with pip

## Steps

### 2.1 Install Apache Airflow

```bash
# Install Airflow
pip install apache-airflow==2.8.1
pip install apache-airflow-providers-http==4.5.1
```

**Screenshot**: Airflow installation

### 2.2 Set Airflow Home Directory

**Windows (PowerShell)**:
```powershell
$env:AIRFLOW_HOME="$PWD\airflow"
```

**Linux/Mac**:
```bash
export AIRFLOW_HOME=$(pwd)/airflow
```

**Screenshot**: Environment variable set

### 2.3 Initialize Airflow Database

```bash
airflow db init
```

**Screenshot**: Database initialization output

### 2.4 Create Airflow Admin User

```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

**Screenshot**: User creation output

### 2.5 Start Airflow Webserver

Open a new terminal and run:

```bash
# Set AIRFLOW_HOME again in this terminal
export AIRFLOW_HOME=$(pwd)/airflow  # Linux/Mac
# OR
$env:AIRFLOW_HOME="$PWD\airflow"  # Windows PowerShell

airflow webserver --port 8080
```

**Screenshot**: Webserver starting

### 2.6 Access Airflow UI

1. Open browser: http://localhost:8080
2. Login with: admin / admin
3. **Screenshot**: Airflow dashboard

### 2.7 Start Airflow Scheduler

Open another new terminal and run:

```bash
# Set AIRFLOW_HOME again
export AIRFLOW_HOME=$(pwd)/airflow  # Linux/Mac
# OR
$env:AIRFLOW_HOME="$PWD\airflow"  # Windows PowerShell

airflow scheduler
```

**Screenshot**: Scheduler running

### 2.8 Create Data Extraction Script

Create `src/data/extract.py`:

```python
"""
Data Extraction Module for OpenWeather API
"""
import os
import json
import requests
from datetime import datetime
from pathlib import Path
import yaml

def load_config():
    config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_api_key():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY environment variable not set")
    return api_key

def fetch_weather_data(city="New York", country_code="US"):
    api_key = get_api_key()
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": f"{city},{country_code}",
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    data["collection_timestamp"] = datetime.utcnow().isoformat()
    return data

def save_raw_data(data, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"weather_raw_{timestamp}.json"
    filepath = output_dir / filename
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    return filepath

def extract_weather_data():
    config = load_config()
    city = config["api"]["openweather"]["city"]
    country_code = config["api"]["openweather"]["country_code"]
    
    data = fetch_weather_data(city, country_code)
    
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "data" / "raw"
    filepath = save_raw_data(data, output_dir)
    
    print(f"Data extracted and saved to: {filepath}")
    return filepath

if __name__ == "__main__":
    extract_weather_data()
```

**Screenshot**: extract.py file created

### 2.9 Test Extraction Script

```bash
python src/data/extract.py
```

**Screenshot**: Successful extraction output and data file

### 2.10 Create Data Quality Check Script

Create `src/data/quality_check.py`:

```python
"""
Data Quality Check Module
"""
import json
import pandas as pd
from pathlib import Path
import sys

def check_null_percentage(df, key_columns, threshold=0.01):
    if df.empty:
        print("ERROR: DataFrame is empty")
        return False
    
    existing_cols = [col for col in key_columns if col in df.columns]
    if not existing_cols:
        print(f"WARNING: None of the key columns {key_columns} found")
        return False
    
    failed_columns = []
    for col in existing_cols:
        null_count = df[col].isnull().sum()
        null_percentage = null_count / len(df)
        if null_percentage > threshold:
            failed_columns.append({
                'column': col,
                'null_percentage': null_percentage
            })
    
    if failed_columns:
        print("ERROR: Data quality check FAILED")
        for col_info in failed_columns:
            print(f"  - {col_info['column']}: {col_info['null_percentage']:.2%} null")
        return False
    
    print(f"Data quality check PASSED: All key columns have <{threshold:.2%} null values")
    return True

def perform_quality_check(data_file):
    with open(data_file, 'r') as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    
    key_columns = ['main.temp', 'main.humidity', 'main.pressure', 'wind.speed', 'dt']
    return check_null_percentage(df, key_columns, threshold=0.01)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = perform_quality_check(Path(sys.argv[1]))
        sys.exit(0 if result else 1)
```

**Screenshot**: quality_check.py file

### 2.11 Update Extract Script with Quality Check

Add to `src/data/extract.py` at the end of `extract_weather_data()`:

```python
from .quality_check import perform_quality_check

# In extract_weather_data() function, after saving:
print("Performing data quality check...")
if not perform_quality_check(filepath):
    print("ERROR: Data quality check failed. DAG will stop.")
    sys.exit(1)
print("Data quality check passed.")
```

**Screenshot**: Updated extract.py

### 2.12 Create Airflow DAG

Create `airflow/dags/weather_prediction_dag.py`:

```python
"""
Apache Airflow DAG for Weather Prediction Pipeline
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.data.extract import extract_weather_data

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
```

**Screenshot**: DAG file created

### 2.13 Verify DAG in Airflow UI

1. Wait a few seconds for Airflow to detect the DAG
2. Refresh the Airflow UI
3. Look for `weather_prediction_pipeline` DAG
4. **Screenshot**: DAG visible in Airflow UI

### 2.14 Test DAG

1. In Airflow UI, toggle the DAG ON
2. Click "Trigger DAG"
3. Watch the task execute
4. **Screenshot**: DAG run successful

### 2.15 Commit Changes

```bash
git add .
git commit -m "Step 2: Airflow setup and extraction DAG created"
```

**Screenshot**: Git commit

## Deliverables Checklist

- [ ] Airflow installed
- [ ] Airflow database initialized
- [ ] Admin user created
- [ ] Webserver running
- [ ] Scheduler running
- [ ] Airflow UI accessible
- [ ] Extraction script created
- [ ] Quality check script created
- [ ] DAG created
- [ ] DAG visible in Airflow UI
- [ ] DAG run successfully
- [ ] Screenshots captured
- [ ] Git commit made

## Next Step

**Member 1**: Proceed to [STEP_3_DVC.md](STEP_3_DVC.md)

**Member 2**: Continue reviewing Member 1's PRs and prepare for your steps.

