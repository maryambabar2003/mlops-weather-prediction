# Step 1: OpenWeather API Setup

## 👤 Assigned to: Member 1

## Objective
Set up OpenWeather API access and configure the project for weather data extraction.

## Prerequisites
- Python 3.8+ installed
- pip installed
- Text editor

## Steps

### 1.1 Get OpenWeather API Key

1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Navigate to API Keys section
4. Generate a new API key
5. **Screenshot**: API key page showing your key (blur sensitive parts)

### 1.2 Create Project Structure

Run these commands:

```bash
# Create project directories
mkdir -p src/data src/models src/api config data/raw data/processed models tests airflow/dags airflow/logs

# Create __init__.py files
touch src/__init__.py
touch src/data/__init__.py
touch src/models/__init__.py
touch src/api/__init__.py
touch tests/__init__.py
```

**Screenshot**: Directory structure

### 1.3 Create Configuration File

Create `config/config.yaml`:

```yaml
api:
  openweather:
    base_url: "https://api.openweathermap.org/data/2.5"
    api_key: "${OPENWEATHER_API_KEY}"
    city: "New York"
    country_code: "US"
    units: "metric"

prediction:
  target_variable: "temperature"
  horizon_hours: 6
  city_name: "New York"
```

**Screenshot**: config.yaml file

### 1.4 Set Environment Variable

**Windows (PowerShell)**:
```powershell
$env:OPENWEATHER_API_KEY="your_api_key_here"
```

**Linux/Mac**:
```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

**Screenshot**: Environment variable set (command output)

### 1.5 Test API Connection

Create a simple test script `test_api.py`:

```python
import os
import requests

api_key = os.getenv("OPENWEATHER_API_KEY")
url = f"https://api.openweathermap.org/data/2.5/weather?q=New York,US&appid={api_key}&units=metric"

response = requests.get(url)
print(f"Status: {response.status_code}")
print(response.json())
```

Run:
```bash
python test_api.py
```

**Screenshot**: Successful API response

### 1.6 Create Requirements File

Create `requirements.txt`:

```
requests==2.31.0
pyyaml==6.0.1
python-dotenv==1.0.0
pandas==2.1.4
numpy==1.26.2
```

Install:
```bash
pip install -r requirements.txt
```

**Screenshot**: Package installation

### 1.7 Initialize Git Repository

```bash
git init
git add .
git commit -m "Step 1: OpenWeather API setup complete"
```

**Screenshot**: Git commit

## Deliverables Checklist

- [ ] OpenWeather API key obtained
- [ ] Project structure created
- [ ] config.yaml created
- [ ] Environment variable set
- [ ] API connection tested successfully
- [ ] requirements.txt created and packages installed
- [ ] Git repository initialized
- [ ] Screenshots captured
- [ ] Git commit made

## Next Step

**Member 1**: Proceed to [STEP_2_AIRFLOW.md](STEP_2_AIRFLOW.md)

**Member 2**: Review Member 1's work and prepare for Step 4. See [COLLABORATION_GUIDE.md](COLLABORATION_GUIDE.md) for details.

