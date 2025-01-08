import requests
import json

# API key and endpoint
API_KEY = '42cb047397fee9639d8da30ed471abe2'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Function to fetch current weather
def fetch_current_weather(city='London'):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        print("API request successful!")
        return response.json()
    else:
        print(f"API Error: {response.status_code}, {response.text}")
        return None

# Fetch and display current weather
current_weather = fetch_current_weather()
if current_weather:
    print(json.dumps(current_weather, indent=4))
