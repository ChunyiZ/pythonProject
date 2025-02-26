import requests
import pandas as pd
from pandas import json_normalize

# API endpoint and key
API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = '42bd74887c364e95855b106a5aa3bf5d'

# Parameters for the API request
params = {
    "country": "us",
    "apiKey": API_KEY
}

# Making the API request
response = requests.get(API_URL, params=params)

if response.status_code == 200:
    # Parsing the JSON response
    data = response.json()
    
    # Normalizing the JSON data to a flat table
    articles = data.get('articles', [])
    df = json_normalize(articles)
    
    # Display the DataFrame
    print(df.head())
else:
    print(f"Error: {response.status_code}")