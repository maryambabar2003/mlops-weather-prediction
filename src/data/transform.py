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

