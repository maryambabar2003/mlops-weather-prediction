"""
Data Quality Check Module
"""
import json
import pandas as pd
from pathlib import Path
import sys

def check_null_percentage(df, key_columns, threshold=0.01):
    if df.empty:
        print("ERROR: DataFrame is empty")
        return False
    
    existing_cols = [col for col in key_columns if col in df.columns]
    if not existing_cols:
        print(f"WARNING: None of the key columns {key_columns} found")
        return False
    
    failed_columns = []
    for col in existing_cols:
        null_count = df[col].isnull().sum()
        null_percentage = null_count / len(df)
        if null_percentage > threshold:
            failed_columns.append({
                'column': col,
                'null_percentage': null_percentage
            })
    
    if failed_columns:
        print("ERROR: Data quality check FAILED")
        for col_info in failed_columns:
            print(f"  - {col_info['column']}: {col_info['null_percentage']:.2%} null")
        return False
    
    print(f"Data quality check PASSED: All key columns have <{threshold:.2%} null values")
    return True

def perform_quality_check(data_file):
    with open(data_file, 'r') as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    
    key_columns = ['main.temp', 'main.humidity', 'main.pressure', 'wind.speed', 'dt']
    return check_null_percentage(df, key_columns, threshold=0.01)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = perform_quality_check(Path(sys.argv[1]))
        sys.exit(0 if result else 1)

