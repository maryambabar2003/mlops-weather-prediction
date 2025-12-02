# Step 6: Docker Containerization

## 👤 Assigned to: Member 2

## Objective
Create FastAPI application for model serving and containerize it with Docker.

## Prerequisites
- Step 5 completed
- Docker installed
- Model training completed (from Step 4)

## Steps

### 6.1 Install FastAPI and Dependencies

```bash
pip install fastapi uvicorn prometheus-client
```

**Screenshot**: Package installation

### 6.2 Create FastAPI Application

Create `src/api/app.py`:

```python
"""
FastAPI Application for Model Serving
"""
import os
import sys
from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import mlflow
import mlflow.sklearn

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Prometheus metrics
REQUEST_COUNT = Counter('api_requests_total', 'Total number of API requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('api_request_latency_seconds', 'API request latency', ['method', 'endpoint'])
PREDICTION_COUNT = Counter('predictions_total', 'Total number of predictions made')
DATA_DRIFT_COUNT = Counter('data_drift_detected_total', 'Number of data drift detections')

app = FastAPI(
    title="Weather Prediction API",
    description="MLOps Real-Time Predictive System",
    version="1.0.0"
)

model = None

def load_model():
    global model
    try:
        models_dir = project_root / "models"
        model_files = list(models_dir.glob("weather_model_*.joblib"))
        if model_files:
            latest_model = max(model_files, key=lambda p: p.stat().st_mtime)
            model = joblib.load(latest_model)
            print(f"Model loaded: {latest_model}")
        else:
            print("Warning: No model found")
    except Exception as e:
        print(f"Error loading model: {e}")

@app.on_event("startup")
async def startup_event():
    load_model()

class PredictionRequest(BaseModel):
    temperature: float = Field(..., description="Current temperature (°C)")
    humidity: float = Field(..., description="Current humidity (%)")
    pressure: float = Field(..., description="Current pressure (hPa)")
    wind_speed: float = Field(..., description="Current wind speed (m/s)")

class PredictionResponse(BaseModel):
    predicted_temperature: float
    timestamp: str

@app.get("/")
async def root():
    return {"message": "Weather Prediction API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    REQUEST_COUNT.labels(method='POST', endpoint='/predict').inc()
    
    with REQUEST_LATENCY.labels(method='POST', endpoint='/predict').time():
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Simple feature vector (adjust based on your model)
        features = [[request.temperature, request.humidity, request.pressure, request.wind_speed]]
        
        try:
            prediction = model.predict(features)[0]
            PREDICTION_COUNT.inc()
            
            return PredictionResponse(
                predicted_temperature=float(prediction),
                timestamp=datetime.utcnow().isoformat()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Screenshot**: app.py file created

### 6.3 Test FastAPI Locally

```bash
# Start the API
python src/api/app.py
```

In another terminal:
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test prediction endpoint
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 20.0, "humidity": 65.0, "pressure": 1013.0, "wind_speed": 5.0}'
```

**Screenshot**: API running and responding

### 6.4 Create Dockerfile

Create `docker/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Screenshot**: Dockerfile created

### 6.5 Update Requirements.txt

Add to `requirements.txt`:

```
fastapi==0.109.0
uvicorn==0.27.0
prometheus-client==0.19.0
```

**Screenshot**: Updated requirements.txt

### 6.6 Build Docker Image

```bash
docker build -f docker/Dockerfile -t weather-prediction-api:latest .
```

**Screenshot**: Docker build output

### 6.7 Run Docker Container

```bash
docker run -d -p 8000:8000 --name weather-api weather-prediction-api:latest
```

**Screenshot**: Container running

### 6.8 Test Container

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test metrics endpoint
curl http://localhost:8000/metrics
```

**Screenshot**: Container health check

### 6.9 Stop and Remove Container

```bash
docker stop weather-api
docker rm weather-api
```

**Screenshot**: Container stopped

### 6.10 Commit Changes

```bash
git add .
git commit -m "Step 6: Docker containerization complete"
git push
```

**Screenshot**: Git commit

## Deliverables Checklist

- [ ] FastAPI application created
- [ ] API tested locally
- [ ] Dockerfile created
- [ ] Docker image built
- [ ] Container runs successfully
- [ ] Health endpoint works
- [ ] Metrics endpoint works
- [ ] Screenshots captured
- [ ] Git commit made

## Next Step

**Member 2**: Proceed to [STEP_7_MONITORING.md](STEP_7_MONITORING.md)

**Member 1**: Help test Docker deployment and prepare for final integration.

