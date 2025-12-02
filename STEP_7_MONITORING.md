# Step 7: Prometheus and Grafana Monitoring

## 👤 Assigned to: Member 2

## Objective
Set up Prometheus and Grafana for monitoring the API and model performance.

## Prerequisites
- Step 6 completed
- Docker and Docker Compose installed

## Steps

### 7.1 Create Prometheus Configuration

Create `docker/prometheus/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'weather-api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'
```

**Screenshot**: Prometheus config file

### 7.2 Create Grafana Data Source Configuration

Create `docker/grafana/datasources/prometheus.yml`:

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

**Screenshot**: Grafana datasource config

### 7.3 Create Docker Compose File

Create `docker/docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI}
    volumes:
      - ../models:/app/models
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/datasources:/etc/grafana/provisioning/datasources

volumes:
  prometheus_data:
  grafana_data:
```

**Screenshot**: docker-compose.yml file

### 7.4 Start Services with Docker Compose

```bash
cd docker
docker-compose up -d
```

**Screenshot**: Services starting

### 7.5 Verify Services Running

```bash
docker-compose ps
```

**Screenshot**: All services running

### 7.6 Access Prometheus UI

1. Open browser: http://localhost:9090
2. Go to Status > Targets
3. Verify "weather-api" target is UP
4. **Screenshot**: Prometheus targets page

### 7.7 Query Prometheus Metrics

In Prometheus UI:
1. Go to Graph
2. Try query: `api_requests_total`
3. Try query: `rate(api_request_latency_seconds_bucket[5m])`
4. **Screenshot**: Prometheus queries

### 7.8 Access Grafana UI

1. Open browser: http://localhost:3000
2. Login: admin / admin
3. Change password when prompted
4. **Screenshot**: Grafana dashboard

### 7.9 Verify Prometheus Data Source

1. Go to Configuration > Data Sources
2. Verify Prometheus is configured
3. Test connection
4. **Screenshot**: Data source connected

### 7.10 Create Grafana Dashboard

1. Go to Dashboards > New Dashboard
2. Add panel for "Request Rate":
   - Query: `rate(api_requests_total[5m])`
3. Add panel for "Request Latency":
   - Query: `histogram_quantile(0.95, api_request_latency_seconds_bucket)`
4. Add panel for "Total Predictions":
   - Query: `predictions_total`
5. Add panel for "Data Drift":
   - Query: `rate(data_drift_detected_total[5m])`
6. Save dashboard
7. **Screenshot**: Grafana dashboard created

### 7.11 Generate Some API Traffic

```bash
# Make some API calls to generate metrics
for i in {1..10}; do
  curl -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    -d '{"temperature": 20.0, "humidity": 65.0, "pressure": 1013.0, "wind_speed": 5.0}'
  sleep 1
done
```

**Screenshot**: API calls made

### 7.12 Verify Metrics in Grafana

1. Refresh Grafana dashboard
2. Verify metrics appear
3. **Screenshot**: Metrics visible in dashboard

### 7.13 Create Grafana Alert

1. Go to Alerting > Alert Rules
2. Create new rule:
   - Name: "High Latency Alert"
   - Condition: `histogram_quantile(0.95, api_request_latency_seconds_bucket) > 0.5`
   - Message: "API latency exceeds 500ms threshold"
3. Save alert
4. **Screenshot**: Alert configured

### 7.14 Test Alert (Optional)

1. Simulate high latency (modify API temporarily)
2. Trigger alert
3. **Screenshot**: Alert firing

### 7.15 Commit Changes

```bash
git add .
git commit -m "Step 7: Prometheus and Grafana monitoring complete"
git push
```

**Screenshot**: Git commit

## Deliverables Checklist

- [ ] Prometheus configuration created
- [ ] Grafana datasource configured
- [ ] Docker Compose file created
- [ ] All services running
- [ ] Prometheus UI accessible
- [ ] Prometheus scraping API metrics
- [ ] Grafana UI accessible
- [ ] Grafana dashboard created
- [ ] Metrics visible in dashboard
- [ ] Alert configured
- [ ] Screenshots captured
- [ ] Git commit made

## Final Steps (Both Members)

**Member 2**:
- [ ] Create final PR from feature branch to `dev`
- [ ] Ensure all monitoring is working

**Both Members**:
- [ ] Review all code together
- [ ] Test complete pipeline end-to-end
- [ ] Review all screenshots
- [ ] Document any issues
- [ ] Create final project summary
- [ ] Merge to `test` branch (with approval)
- [ ] Merge to `master` branch (with approval)
- [ ] Prepare presentation materials

## Project Complete! 🎉

All components of the MLOps Real-Time Predictive System have been implemented.

