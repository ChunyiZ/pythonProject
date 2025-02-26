import requests
import pandas as pd
import matplotlib.pyplot as plt

# Configuration
API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = '42bd74887c364e95855b106a5aa3bf5d'  # Replace with valid key

def fetch_news():
    """Simplified data fetching function"""
    params = {
        'country': 'us',
        'apiKey': API_KEY,
        'pageSize': 100  # Max allowed items
    }
    response = requests.get(API_URL, params=params)
    return response.json()['articles']  # Directly return article list

def analyze_data(articles):
    """Core data analysis pipeline"""
    df = pd.DataFrame(articles)
    
    # Data cleaning
    df = df[df['content'].notna()]  # Filter out empty content
    df['source'] = df['source'].apply(lambda x: x['name'])
    
    # Feature engineering
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['title_length'] = df['title'].str.len()
    
    return df

# Execution flow
if __name__ == "__main__":
    news_articles = fetch_news()
    df_processed = analyze_data(news_articles)
    
    # Generate report
    print(f"📈 Analysis Results ({len(df_processed)} valid articles)")
    print("Top Sources:\n", df_processed['source'].value_counts().head(3))
    
    # Visualize title lengths
    plt.hist(df_processed['title_length'], 
             bins=15, 
             color='skyblue', 
             edgecolor='black')
    plt.title('News Title Length Distribution')
    plt.xlabel('Character Count')
    plt.ylabel('Article Count')
    plt.show()
