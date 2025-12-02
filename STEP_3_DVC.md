# Step 3: Data Version Control (DVC) Setup

## 👤 Assigned to: Member 1

## Objective
Set up DVC for versioning processed datasets and configure remote storage.

## Prerequisites
- Step 2 completed
- Git repository initialized

## Steps

### 3.1 Install DVC

```bash
pip install dvc dvc-s3
```

**Screenshot**: DVC installation

### 3.2 Initialize DVC

```bash
dvc init
```

**Screenshot**: DVC initialization output

### 3.3 Create .dvcignore File

Create `.dvcignore`:

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist/
build/
.eggs/
venv/
env/
.venv
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db
*.log
.pytest_cache/
.coverage
htmlcov/
airflow/logs/
airflow/airflow.db
mlruns/
.env
```

**Screenshot**: .dvcignore file

### 3.4 Commit DVC Initialization

```bash
git add .dvcignore .dvc/.gitignore
git commit -m "Initialize DVC"
```

**Screenshot**: Git commit

### 3.5 Create Transformation Script (Basic)

Create `src/data/transform.py`:

```python
"""
Data Transformation Module
"""
import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import yaml

def load_latest_raw_data(raw_data_dir):
    json_files = list(raw_data_dir.glob("weather_raw_*.json"))
    if not json_files:
        raise FileNotFoundError("No raw data files found")
    latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
    with open(latest_file, "r") as f:
        data = json.load(f)
    return pd.json_normalize(data)

def create_time_features(df):
    df = df.copy()
    if 'dt' in df.columns:
        df['datetime'] = pd.to_datetime(df['dt'], unit='s')
    elif 'collection_timestamp' in df.columns:
        df['datetime'] = pd.to_datetime(df['collection_timestamp'])
    else:
        df['datetime'] = pd.to_datetime(datetime.utcnow())
    
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['month'] = df['datetime'].dt.month
    
    # Cyclical encoding
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    
    return df

def transform_weather_data():
    project_root = Path(__file__).parent.parent.parent
    raw_data_dir = project_root / "data" / "raw"
    processed_data_dir = project_root / "data" / "processed"
    
    df = load_latest_raw_data(raw_data_dir)
    df = create_time_features(df)
    
    processed_data_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_file = processed_data_dir / f"weather_processed_{timestamp}.parquet"
    df.to_parquet(output_file, index=False)
    
    print(f"Data transformed and saved to: {output_file}")
    return output_file

if __name__ == "__main__":
    transform_weather_data()
```

**Screenshot**: transform.py file

### 3.6 Test Transformation

```bash
python src/data/transform.py
```

**Screenshot**: Transformation output and processed file

### 3.7 Add Processed Data to DVC

```bash
# Add the processed data directory to DVC
dvc add data/processed/

# Check status
dvc status
```

**Screenshot**: DVC add output and status

### 3.8 Commit DVC Metadata

```bash
git add data/processed/.gitignore data/processed/*.dvc
git commit -m "Add processed data to DVC"
```

**Screenshot**: Git commit with .dvc files

### 3.9 Configure DVC Remote (Dagshub - will complete in Step 4)

For now, note that you'll configure the remote in Step 4:

```bash
# This will be done in Step 4 after Dagshub setup
# dvc remote add -d dagshub https://dagshub.com/your-username/your-repo.dvc
```

**Screenshot**: Note in documentation

### 3.10 Update Airflow DAG

Add transformation task to `airflow/dags/weather_prediction_dag.py`:

```python
from src.data.transform import transform_weather_data

transform_task = PythonOperator(
    task_id='transform_weather_data',
    python_callable=transform_weather_data,
    dag=dag,
)

# Update dependencies
extract_task >> transform_task
```

**Screenshot**: Updated DAG file

### 3.11 Test Updated DAG

1. Refresh Airflow UI
2. Trigger the DAG
3. Verify both tasks complete
4. **Screenshot**: DAG run with both tasks

### 3.12 Commit Changes

```bash
git add .
git commit -m "Step 3: DVC setup and transformation task added"
```

**Screenshot**: Git commit

## Deliverables Checklist

- [ ] DVC installed
- [ ] DVC initialized
- [ ] .dvcignore created
- [ ] Transformation script created
- [ ] Transformation tested
- [ ] Data added to DVC
- [ ] DVC metadata committed to Git
- [ ] DAG updated with transformation task
- [ ] DAG tested successfully
- [ ] Screenshots captured
- [ ] Git commit made

## Next Step

**Member 1**: 
- [ ] Create PR from your feature branch to `dev`
- [ ] Notify Member 2 that data pipeline is ready
- [ ] Wait for Member 2's review and merge

**Member 2**: 
- [ ] Review Member 1's PR for Steps 1-3
- [ ] Merge to `dev` after approval
- [ ] Pull latest `dev` branch
- [ ] Proceed to [STEP_4_MLFLOW_DAGSHUB.md](STEP_4_MLFLOW_DAGSHUB.md)

