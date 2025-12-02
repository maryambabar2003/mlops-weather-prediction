# Step 4: MLflow and Dagshub Integration

## 👤 Assigned to: Member 2

## ⚠️ Prerequisite
Wait for Member 1 to complete Steps 1-3 and merge to `dev` branch before starting.

## Objective
Set up Dagshub repository, configure MLflow tracking, and create model training script.

## Prerequisites
- Step 3 completed
- GitHub account (for Dagshub)

## Steps

### 4.1 Create Dagshub Account and Repository

1. Go to https://dagshub.com
2. Sign up with GitHub
3. Click "New Repository"
4. Name: `mlops-weather-prediction` (or your choice)
5. Initialize with README (optional)
6. Create repository
7. **Screenshot**: Dagshub repository created

### 4.2 Link Git Repository to Dagshub

```bash
# Add Dagshub as remote
git remote add dagshub https://dagshub.com/your-username/your-repo.git

# Verify remotes
git remote -v
```

**Screenshot**: Git remotes configured

### 4.3 Get Dagshub MLflow Tracking URI

1. In Dagshub repository, go to "Remote" tab
2. Copy the MLflow Tracking URI (format: `https://dagshub.com/your-username/your-repo.mlflow`)
3. **Screenshot**: MLflow URI from Dagshub

### 4.4 Set MLflow Tracking URI

**Windows (PowerShell)**:
```powershell
$env:MLFLOW_TRACKING_URI="https://dagshub.com/your-username/your-repo.mlflow"
```

**Linux/Mac**:
```bash
export MLFLOW_TRACKING_URI="https://dagshub.com/your-username/your-repo.mlflow"
```

**Screenshot**: Environment variable set

### 4.5 Get Dagshub Access Token

1. Go to Dagshub Settings > Access Tokens
2. Create new token with DVC read/write permissions
3. Copy the token
4. **Screenshot**: Token creation (blur sensitive parts)

### 4.6 Configure DVC Remote

```bash
# Configure DVC remote to Dagshub
dvc remote add -d dagshub https://dagshub.com/your-username/your-repo.dvc
dvc remote modify dagshub user your-username
dvc remote modify dagshub password your-dagshub-token

# Verify configuration
cat .dvc/config
```

**Screenshot**: DVC remote configuration

### 4.7 Install MLflow

```bash
pip install mlflow scikit-learn pandas-profiling
```

**Screenshot**: MLflow installation

### 4.8 Create Model Training Script

Create `src/models/train.py`:

```python
"""
Model Training Script with MLflow Tracking
"""
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mlflow
import mlflow.sklearn
from datetime import datetime
import joblib
import yaml

def load_config():
    config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def load_processed_data(data_dir):
    parquet_files = list(data_dir.glob("weather_processed_*.parquet"))
    if not parquet_files:
        raise FileNotFoundError("No processed data files found")
    latest_file = max(parquet_files, key=lambda p: p.stat().st_mtime)
    return pd.read_parquet(latest_file)

def prepare_features(df, target_col='main.temp'):
    exclude_cols = [target_col, 'datetime', 'dt', 'collection_timestamp']
    feature_cols = [col for col in df.columns if col not in exclude_cols and df[col].dtype in ['float64', 'int64']]
    feature_cols = [col for col in feature_cols if not df[col].isna().all()]
    X = df[feature_cols].fillna(0)
    y = df[target_col]
    return X, y

def train_model(X_train, y_train, hyperparameters):
    model = RandomForestRegressor(
        n_estimators=hyperparameters.get('n_estimators', 100),
        max_depth=hyperparameters.get('max_depth', 10),
        min_samples_split=hyperparameters.get('min_samples_split', 2),
        min_samples_leaf=hyperparameters.get('min_samples_leaf', 1),
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X, y):
    y_pred = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    return {'rmse': rmse, 'mae': mae, 'r2_score': r2}

def train_weather_model():
    config = load_config()
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data" / "processed"
    
    df = load_processed_data(data_dir)
    target_col = "main.temp"
    X, y = prepare_features(df, target_col=target_col)
    
    if len(X) > 1:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    else:
        X_train, y_train = X, y
        X_test, y_test = X, y
    
    mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    if mlflow_tracking_uri:
        mlflow.set_tracking_uri(mlflow_tracking_uri)
    
    experiment_name = "weather_prediction"
    mlflow.set_experiment(experiment_name)
    
    hyperparameters = {
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 2,
        'min_samples_leaf': 1
    }
    
    with mlflow.start_run(run_name=f"training_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"):
        mlflow.log_params(hyperparameters)
        
        model = train_model(X_train, y_train, hyperparameters)
        
        train_metrics = evaluate_model(model, X_train, y_train)
        test_metrics = evaluate_model(model, X_test, y_test)
        
        mlflow.log_metrics({
            'train_rmse': train_metrics['rmse'],
            'train_mae': train_metrics['mae'],
            'train_r2_score': train_metrics['r2_score'],
            'test_rmse': test_metrics['rmse'],
            'test_mae': test_metrics['mae'],
            'test_r2_score': test_metrics['r2_score'],
        })
        
        mlflow.sklearn.log_model(model, "model")
        
        models_dir = project_root / "models"
        models_dir.mkdir(exist_ok=True)
        model_path = models_dir / f"weather_model_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.joblib"
        joblib.dump(model, model_path)
        
        print(f"Model trained and logged to MLflow")
        print(f"Metrics - RMSE: {test_metrics['rmse']:.2f}, MAE: {test_metrics['mae']:.2f}, R²: {test_metrics['r2_score']:.2f}")
        
        return str(model_path)

if __name__ == "__main__":
    train_weather_model()
```

**Screenshot**: train.py file created

### 4.9 Test Training Script

```bash
python src/models/train.py
```

**Screenshot**: Training output with metrics

### 4.10 Verify MLflow Experiment in Dagshub

1. Go to Dagshub repository
2. Navigate to "Experiments" tab
3. Verify experiment appears
4. **Screenshot**: MLflow experiment in Dagshub

### 4.11 Update Airflow DAG

Add training task to `airflow/dags/weather_prediction_dag.py`:

```python
from src.models.train import train_weather_model

train_task = PythonOperator(
    task_id='train_weather_model',
    python_callable=train_weather_model,
    dag=dag,
)

# Update dependencies
extract_task >> transform_task >> train_task
```

**Screenshot**: Updated DAG with training task

### 4.12 Test Complete DAG

1. Trigger DAG in Airflow UI
2. Verify all three tasks complete
3. **Screenshot**: Complete DAG run

### 4.13 Push Data to DVC Remote

```bash
# Push data to Dagshub
dvc push

# Verify in Dagshub
```

**Screenshot**: DVC push successful

### 4.14 Commit and Push to Dagshub

```bash
git add .
git commit -m "Step 4: MLflow and Dagshub integration complete"
git push dagshub main
```

**Screenshot**: Git push to Dagshub

## Deliverables Checklist

- [ ] Dagshub account created
- [ ] Dagshub repository created
- [ ] Git remote added
- [ ] MLflow tracking URI configured
- [ ] DVC remote configured
- [ ] Training script created
- [ ] Training tested successfully
- [ ] MLflow experiment visible in Dagshub
- [ ] DAG updated with training task
- [ ] Complete DAG tested
- [ ] Data pushed to DVC remote
- [ ] Code pushed to Dagshub
- [ ] Screenshots captured
- [ ] Git commit made

## Next Step

**Member 2**: Proceed to [STEP_5_CICD.md](STEP_5_CICD.md)

**Member 1**: Review Member 2's PRs and help test the integration.

