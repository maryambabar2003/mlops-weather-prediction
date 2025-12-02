import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")

if not api_key:
    print("ERROR: OPENWEATHER_API_KEY not found in environment or .env file")
    print("Please check:")
    print("1. .env file exists in project root")
    print("2. .env file contains: OPENWEATHER_API_KEY=your_key_here")
    exit(1)

print(f"API Key loaded: {api_key[:8]}...{api_key[-4:]}")  # Show partial key for verification

url = f"https://api.openweathermap.org/data/2.5/weather?q=New York,US&appid={api_key}&units=metric"

response = requests.get(url)
print(f"Status: {response.status_code}")
print(response.json())