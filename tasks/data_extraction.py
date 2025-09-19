import prefect
from prefect import task
from datetime import datetime, timedelta
import requests
import json
import os
import time
import hashlib
from dotenv import load_dotenv

load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

API_CONFIGS = [
    {
        "name": "FMP",
        "url": "https://financialmodelingprep.com/api/v4/general_news",
        "params":{"page": 0, "apikey": f"{FMP_API_KEY}"},
        "title_key": "title",
        "link_key": "url",
        "date_key": "publishedDate",
    },
    {
        "name": "Alpha Vantage",
        "url": "https://www.alphavantage.co/query",
        "params": {"function": "NEWS_SENTIMENT", "apikey": f"{ALPHA_VANTAGE_KEY}"},
        "title_key": "title",
        "link_key": "url",
        "date_key": "time_published",
    },
    {
        "name": "NewsAPI",
        "url": "https://newsapi.org/v2/top-headlines",
        "params": {"category": "business", "apiKey": f"{NEWSAPI_KEY}"},
        "title_key": "title",
        "link_key": "url",
        "date_key": "publishedAt",
    }
]


@task
# --- Extract step ---
def extract_news(**context):
    news_data = []
    seen_headlines = set()  # For deduplication within a run

    for api in API_CONFIGS:
        try:
            response = requests.get(api["url"], params=api["params"], timeout=10)
            response.raise_for_status()
            data = response.json()

            # Handle different API response structures
            articles = data.get("articles", data) if api["name"] == "NewsAPI" else \
                      data.get("feed", data) if api["name"] == "Alpha Vantage" else data

            for article in articles:
                title = article.get(api["title_key"])
                if not title:
                    continue
                # Create unique key for deduplication
                unique_key = hashlib.md5(f"{title}_{article.get(api['date_key'], '')}".encode()).hexdigest()
                if unique_key not in seen_headlines:
                    seen_headlines.add(unique_key)
                    news_data.append({
                        "title": title,
                        "link": article.get(api["link_key"]),
                        "published": article.get(api["date_key"]),
                        "source": api["name"]
                    })
            time.sleep(1)  # Respect rate limits
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from {api['name']}: {e}")

    # Save raw JSON
    os.makedirs("/tmp/financial_news", exist_ok=True)
    with open("/tmp/financial_news/raw_news.json", "w") as f:
        json.dump(news_data, f)

    return news_data
