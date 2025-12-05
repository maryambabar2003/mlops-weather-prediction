"""
Data Extraction Module for OpenWeather API
"""
import os
import json
import requests
from datetime import datetime
from pathlib import Path
import yaml
import sys

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    project_root = Path(__file__).parent.parent.parent
    load_dotenv(project_root / ".env")
except ImportError:
    pass  # dotenv not available, rely on system environment variables

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
    
    # Perform data quality check
    print("Performing data quality check...")
    try:
        from .quality_check import perform_quality_check
    except ImportError:
        # Fallback for when running as script
        from quality_check import perform_quality_check
    if not perform_quality_check(filepath):
        print("ERROR: Data quality check failed. DAG will stop.")
        sys.exit(1)
    print("Data quality check passed.")
    
    return filepath



if __name__ == "__main__":
    extract_weather_data()

