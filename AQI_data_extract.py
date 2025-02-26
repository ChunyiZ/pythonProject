import requests
from datetime import datetime, timedelta
import pandas as pd

def create_request_payload(start_date, end_date):
    """Create the request payload for the API call."""
    print("Creating request payload...")
    payload = {
        'lst': start_date.strftime('%Y-%m-%d %H:%M:%S'),
        'lst_aqi': end_date.strftime('%Y-%m-%d %H:%M:%S'),
        'limit': 1000,
        'offset': 0
    }
    print(f"Payload created: {payload}")
    return payload

def get_aqi_data(start_date, end_date, api_key):
    """Fetch AQI data from the API."""
    print("Starting to fetch AQI data...")
    url = "https://data.sh.gov.cn/interface/1124/10185"
    headers = {
        'Content-Type': 'application/json',
        'cache-control': 'no-cache',
        'token': api_key  # Ensure this token is correct and active
    }
    
    payload = create_request_payload(start_date, end_date)
    print(f"Sending POST request to API with payload: {payload}")
    response = requests.post(url, headers=headers, json=payload)
    print(f"Response received with status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('code') == '000000':
            print("Data retrieval successful, processing data...")
            return data.get('data', {}).get('data', [])
        else:
            print(f"Error in response: {data.get('message', 'Unknown error')}")
            return None
    else:
        print(f"Failed to retrieve data: HTTP status {response.status_code}")
        return None

def generate_date_range(days):
    """Generate the date range for the last 'days' days."""
    print(f"Generating date range for the last {days} days...")
    end_date = datetime.now() - timedelta(days=1)  # End date as yesterday
    start_date = end_date - timedelta(days=days)
    print(f"Date range: Start Date = {start_date}, End Date = {end_date}")
    return start_date, end_date

def get_aqi_data_for_last_10_days(api_key):
    """Retrieve and process AQI data for the last 10 days."""
    print("Getting AQI data for the last 10 days...")
    start_date, end_date = generate_date_range(10)
    data_entries = get_aqi_data(start_date, end_date, api_key)
    if data_entries:
        print("AQI data retrieved and processed successfully.")
        return pd.DataFrame(data_entries)
    else:
        print("No AQI data retrieved.")
        return pd.DataFrame()

# Example usage
api_key = '3aa1458ff8e05c7163392d37c4de4bf5'  # Replace with your actual API token
aqi_data = get_aqi_data_for_last_10_days(api_key)

# Save to a CSV file
if not aqi_data.empty:
    print("Saving data to CSV file...")
    aqi_data.to_csv('aqi_data_last_10_days.csv', index=False)
    print("Data saved to 'aqi_data_last_10_days.csv'")
else:
    print("No data to save.")