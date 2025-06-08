import os
import datetime
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import yfinance as yf

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔍 Analyze sentiment from a news snippet
def analyze_sentiment(text):
    prompt = (
        "What is the overall sentiment of the following news content? "
        "Respond with one word only: Positive, Negative, or Neutral.\n\n" + text
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=10
    )
    sentiment = response.choices[0].message.content.strip().capitalize()
    if sentiment not in ["Positive", "Negative", "Neutral"]:
        sentiment = "Neutral"  # fallback
    return sentiment

# 📈 Forecast stock market reaction from multiple headlines
def forecast_market(news_items):
    combined_news = "\n".join(
        [item.get("content") or item.get("description") or item.get("title") for item in news_items]
    )

    prompt = f"""
You are a financial analyst. Based on the following geopolitical news headlines and summaries, forecast how the stock market is likely to react the next day (Bullish, Bearish, or Neutral). Justify your answer briefly in 2-3 lines.

News:
{combined_news}

Your Forecast:
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=200
    )

    forecast = response.choices[0].message.content.strip()
    
    # Extract the first keyword only if it exists
    keyword = forecast.split()[0].capitalize()
    if keyword not in ["Bullish", "Bearish", "Neutral"]:
        keyword = "Neutral"

    save_forecast(keyword)
    return forecast

# 💾 Save forecast to forecast_history.csv
def save_forecast(prediction: str):
    today = datetime.date.today().isoformat()
    df = pd.DataFrame([{
        "date": today,
        "prediction": str(prediction),  # store clean keyword only
        "actual": None
    }])
    df.to_csv("forecast_history.csv", mode='a', header=not os.path.exists("forecast_history.csv"), index=False)

# 📉 Fetch actual S&P 500 movement based on close vs open
def get_actual_market_movement(ticker="^GSPC"):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    data = yf.download(ticker, start=yesterday, end=today)
    if data.empty:
        return None

    open_price = data["Open"].iloc[0]
    close_price = data["Close"].iloc[0]

    if close_price > open_price:
        return "Bullish"
    elif close_price < open_price:
        return "Bearish"
    else:
        return "Neutral"
