# Airflow 2.8.1 Windows Compatibility Issues

## Known Issues

Airflow 2.8.1 has several Windows compatibility problems:

1. **SQLite Path Validation Bug**: Incorrectly rejects valid Windows absolute paths
2. **Flask-Session API Changes**: Import paths have changed in newer versions
3. **Signal Module**: Uses Unix-only signals (SIGALRM) not available on Windows

## Solutions

### Option 1: Use Docker (RECOMMENDED)

This is the most reliable solution for Windows:

```powershell
# Pull Airflow image
docker pull apache/airflow:2.8.1

# Run Airflow standalone (includes webserver, scheduler, and database)
docker run -d \
  --name airflow \
  -p 8080:8080 \
  -v D:\MLOPsProject\airflow\dags:/opt/airflow/dags \
  -v D:\MLOPsProject\airflow\logs:/opt/airflow/logs \
  apache/airflow:2.8.1 standalone

# Access Airflow UI at http://localhost:8080
# Default credentials: airflow / airflow
```

### Option 2: Use WSL (Windows Subsystem for Linux)

If you have WSL installed:

```bash
# In WSL terminal
cd /mnt/d/MLOPsProject
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init
airflow users create --username maryam --firstname Maryam --lastname Khan --role Admin --email maryamkhan2003babar@gmail.com --password admin
```

### Option 3: Continue with Patches (Current Status)

We've applied patches to:
- ✅ Bypassed SQLite path validation
- ✅ Fixed flask_session import
- ⚠️ Still need to fix flask_session API compatibility
- ⚠️ Need to fix signal module issue

**Current blockers:**
- Flask-Session API mismatch (SqlAlchemySessionInterface signature changed)
- Signal.SIGALRM not available on Windows

## Recommendation

**Use Docker** - It's the cleanest solution and avoids all Windows compatibility issues. You can continue with the project steps using Docker, and all your DAGs will work the same way.

## Next Steps

1. Install Docker Desktop for Windows
2. Use the Docker command above
3. Continue with Step 2.5 (Start Airflow Webserver) - it's already running in Docker
4. Access UI at http://localhost:8080
5. Proceed with creating DAGs

