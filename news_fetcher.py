import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(query="geopolitics", sources="bbc-news,reuters", max_articles=10):
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize={max_articles}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return [{"title": a["title"], "content": a["description"], "url": a["url"]} for a in articles]
