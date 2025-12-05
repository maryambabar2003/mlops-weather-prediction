# Docker Setup Summary

## Overview

All steps from Step 2 onwards now use Docker to avoid Windows compatibility issues with Airflow 2.8.1.

## Docker Services

### Step 2: Airflow
- **File**: `docker/airflow-docker-compose.yml`
- **Services**: postgres, airflow-webserver, airflow-scheduler, airflow-init
- **Ports**: 
  - Airflow UI: http://localhost:8080
  - PostgreSQL: 5432 (internal)

### Step 6: API Service
- **File**: `docker/Dockerfile` (for API)
- **Service**: FastAPI application
- **Port**: 8000

### Step 7: Monitoring
- **File**: `docker/monitoring-docker-compose.yml` (or added to airflow compose)
- **Services**: prometheus, grafana
- **Ports**:
  - Prometheus: http://localhost:9090
  - Grafana: http://localhost:3000

## Quick Commands

### Start Airflow
```powershell
cd docker
docker-compose -f airflow-docker-compose.yml up -d
```

### Stop Airflow
```powershell
cd docker
docker-compose -f airflow-docker-compose.yml down
```

### View Logs
```powershell
docker-compose -f docker/airflow-docker-compose.yml logs -f
```

### Access Airflow Container
```powershell
docker-compose -f docker/airflow-docker-compose.yml exec airflow-webserver bash
```

### Install Packages in Airflow Container
```powershell
docker-compose -f docker/airflow-docker-compose.yml exec airflow-webserver pip install package-name
docker-compose -f docker/airflow-docker-compose.yml exec airflow-scheduler pip install package-name
```

## Environment Variables

Create `.env` file in project root:
```env
AIRFLOW_UID=50000
AIRFLOW_PROJECT_DIR=D:/MLOPsProject
_AIRFLOW_WWW_USER_USERNAME=maryam
_AIRFLOW_WWW_USER_PASSWORD=admin
OPENWEATHER_API_KEY=your_key_here
MLFLOW_TRACKING_URI=your_mlflow_uri
```

## Volume Mounts

The Docker Compose file mounts:
- `./airflow/dags` → `/opt/airflow/dags` (DAG files)
- `./airflow/logs` → `/opt/airflow/logs` (Airflow logs)
- `./airflow/plugins` → `/opt/airflow/plugins` (Airflow plugins)

This means DAGs you create in `airflow/dags/` will automatically appear in Airflow UI.

## Troubleshooting

### Containers not starting
```powershell
docker-compose -f docker/airflow-docker-compose.yml logs
```

### DAG not appearing
- Check DAG file is in `airflow/dags/` directory
- Check container logs for Python errors
- Verify imports work (test locally first)

### Permission issues
- Ensure AIRFLOW_UID is set in .env
- Check file permissions on Windows

### Port conflicts
- Change ports in docker-compose.yml if 8080, 9090, or 3000 are in use

