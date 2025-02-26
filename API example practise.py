import requests

# Replace 'API_KEY' with your actual API key from NewsAPI
API_KEY = '42bd74887c364e95855b106a5aa3bf5d'
url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={API_KEY}"
response = requests.get(url)
print(response.status_code)