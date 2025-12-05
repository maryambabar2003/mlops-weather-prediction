# Airflow Windows SQLite Path Issue - Workaround

## Problem
Airflow 2.8.1 has a bug on Windows that incorrectly validates SQLite database paths, preventing initialization.

## Solution: Use Default Airflow Home

Since the custom AIRFLOW_HOME path causes issues, use the default location and configure DAGs folder:

1. **Don't set AIRFLOW_HOME** - Let Airflow use default: `C:\Users\<username>\airflow`

2. **Initialize Airflow** (will use default location):
   ```powershell
   # Clear any AIRFLOW_HOME setting
   Remove-Item Env:\AIRFLOW_HOME -ErrorAction SilentlyContinue
   
   # Initialize database
   airflow db init
   ```

3. **Create user**:
   ```powershell
   airflow users create --username maryam --firstname Maryam --lastname Khan --role Admin --email maryamkhan2003babar@gmail.com --password admin
   ```

4. **Update DAGs folder** to point to your project:
   - Edit: `C:\Users\<username>\airflow\airflow.cfg`
   - Find: `dags_folder = ...`
   - Change to: `dags_folder = D:\MLOPsProject\airflow\dags`

5. **Start Airflow**:
   ```powershell
   airflow webserver --port 8080
   # In another terminal:
   airflow scheduler
   ```

## Alternative: Use Docker (Recommended for Windows)

If the above doesn't work, use Docker:
```powershell
docker run -d -p 8080:8080 -v D:\MLOPsProject\airflow\dags:/opt/airflow/dags apache/airflow:2.8.1 standalone
```

This avoids the Windows path issues entirely.

