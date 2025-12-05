# Quick Start Guide - Docker Setup

## Prerequisites Checklist

- [ ] Docker Desktop installed and running
- [ ] Step 1 completed (API key in .env file)
- [ ] Project structure created

## Quick Start Commands

### 1. Verify Docker is Running

```powershell
docker --version
docker ps
```

### 2. Set Up Environment Variables

Create/update `.env` file in project root:
```env
OPENWEATHER_API_KEY=your_key_here
AIRFLOW_UID=50000
AIRFLOW_PROJECT_DIR=D:/MLOPsProject
_AIRFLOW_WWW_USER_USERNAME=maryam
_AIRFLOW_WWW_USER_PASSWORD=admin
```

### 3. Start Airflow

```powershell
cd docker
docker-compose -f airflow-docker-compose.yml up -d
```

### 4. Wait for Services to Start

```powershell
# Check status
docker-compose -f airflow-docker-compose.yml ps

# Watch logs
docker-compose -f airflow-docker-compose.yml logs -f
```

Wait until you see:
- `airflow-init` shows "exited (0)"
- `airflow-webserver` and `airflow-scheduler` show "Up"

### 5. Access Airflow UI

- URL: http://localhost:8080
- Username: `maryam`
- Password: `admin`

### 6. Install Python Packages in Containers

```powershell
docker-compose -f docker/airflow-docker-compose.yml exec airflow-webserver pip install requests pyyaml pandas python-dotenv
docker-compose -f docker/airflow-docker-compose.yml exec airflow-scheduler pip install requests pyyaml pandas python-dotenv
```

## Common Commands

### Stop Services
```powershell
docker-compose -f docker/airflow-docker-compose.yml down
```

### Restart Services
```powershell
docker-compose -f docker/airflow-docker-compose.yml restart
```

### View Logs
```powershell
# All services
docker-compose -f docker/airflow-docker-compose.yml logs

# Specific service
docker-compose -f docker/airflow-docker-compose.yml logs airflow-webserver
```

### Access Container Shell
```powershell
docker-compose -f docker/airflow-docker-compose.yml exec airflow-webserver bash
```

## Troubleshooting

### Port 8080 already in use
Change port in docker-compose.yml:
```yaml
ports:
  - "8081:8080"  # Use 8081 instead
```

### Containers keep restarting
Check logs:
```powershell
docker-compose -f docker/airflow-docker-compose.yml logs
```

### DAG not appearing
1. Check DAG file is in `airflow/dags/` directory
2. Check for Python errors in logs
3. Verify file permissions

### Can't connect to database
Wait longer for postgres to be ready, or restart:
```powershell
docker-compose -f docker/airflow-docker-compose.yml restart postgres
```

