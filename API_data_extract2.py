import requests
import datetime
import pandas as pd

def create_request_payload(start_date, end_date):
    print("Creating request payload...")
    payload = {
        'lst': start_date.strftime('%Y-%m-%d'),
        'lst_aqi': end_date.strftime('%Y-%m-%d'),
        'limit': 1000,
        'offset': 0
    }
    print(f"Payload: {payload}")
    return payload

def get_aqi_data(city, start_date, end_date, api_key):
    print("Starting get_aqi_data function...")
    url = "https://data.sh.gov.cn/interface/1124/6068"  # Replace with actual endpoint
    headers = {
        'Content-Type': 'application/json',
        'cache-control': 'no-cache',
        'token': api_key
    }
    
    payload = create_request_payload(start_date, end_date)
    
    print("Sending POST request to API...")
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.content.decode()}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Parsed Data: {data}")
        except ValueError:
            print("Error: Response is not in JSON format")
            return None

        if isinstance(data, dict) and 'code' in data and data['code'] == '000000':
            print("Parsing AQI data...")
            aqi_data = []
            data_entries = data.get('data', {}).get('data', [])
            for entry in data_entries:
                aqi_entry = {
                    'start_date': entry.get('lst'),
                    'end_date': entry.get('lst_aqi'),
                    'group_id': entry.get('groupid'),
                    'group_name': entry.get('groupname'),
                    'aqi_item_id': entry.get('aqiitemid'),
                    'aqi_item_name': entry.get('aqiitemname'),
                    'aqi_value': entry.get('aqivalue'),
                    'aqi': entry.get('aqi'),
                    'grade': entry.get('grade'),
                    'quality': entry.get('quality')
                }
                aqi_data.append(aqi_entry)
            print("AQI data parsed successfully.")
            return aqi_data
        else:
            print(f"Error in response: {data.get('message', 'Unknown error')}")
            return None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

def generate_date_range(days):
    print(f"Generating date range for the last {days} days...")
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days)
    print(f"Start Date: {start_date}, End Date: {end_date}")
    return start_date, end_date

def get_aqi_data_for_last_30_days(city, api_key):
    print("Getting AQI data for the last 30 days...")
    start_date, end_date = generate_date_range(30)
    
    aqi_data = get_aqi_data(city, start_date, end_date, api_key)
    if aqi_data:
        print("AQI data retrieved successfully.")
        return pd.DataFrame(aqi_data)
    else:
        print("No AQI data retrieved.")
        return pd.DataFrame()

# Example usage
print("Starting AQI data extraction script...")
api_key = '417d35e242ddf362309c83012da2b406'  # Replace with your actual API key
city = 'Shanghai'
aqi_data = get_aqi_data_for_last_30_days(city, api_key)

# Save to a CSV file
if not aqi_data.empty:
    print("Saving data to CSV file...")
    aqi_data.to_csv('shanghai_aqi_data_last_30_days.csv', index=False)
    print("Data saved to shanghai_aqi_data_last_30_days.csv")
else:
    print("No data to save.")
print("Script finished.")