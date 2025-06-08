# 🌍 GeoPulse AI — Real-Time Geopolitical News Sentiment & Market Forecaster

GeoPulse AI is an intelligent dashboard that fuses **real-time news sentiment analysis** with **financial forecasting**, helping you understand how **geopolitical developments** could influence the **stock market (S&P 500)** the next day.

> 📈 “Can AI predict how today’s news will shape tomorrow’s markets?”  
GeoPulse AI was built to explore that idea — from scratch.

---

## 🔧 Built With

- 🧠 **OpenAI API** (GPT-3.5-turbo) — for sentiment and forecast generation  
- 📰 **NewsAPI** — to fetch latest geopolitical headlines  
- 💹 **Yahoo Finance (yfinance)** — for S&P 500 actual market data  
- 📊 **Plotly** — for beautiful, interactive forecast accuracy charts  
- 🐍 Python + **Streamlit** — for a slick, no-hassle front-end

---

## ✨ Features

- 🔍 **Enter a topic** → Automatically fetch news articles
- 💬 **Analyze sentiment** (Positive / Neutral / Negative) per article
- 🧠 **Generate market forecast** (Bullish / Bearish / Neutral) based on the day's news
- 📈 **Fetch actual market movement** (S&P 500 daily close delta)
- 📊 **Track forecasting accuracy** over time
- 📉 **Visualize market vs AI predictions** in one unified chart

---

## 📸 Demo Preview

<img width="1511" alt="Screenshot 2025-06-08 at 5 54 43 PM" src="https://github.com/user-attachments/assets/4a06e540-8527-4a80-bed6-e01cb239fb93" />

---

## 📦 Project Structure

geopulse-ai/
│
├── app.py # Main Streamlit app
├── news_fetcher.py # NewsAPI fetch logic
├── sentiment_forecaster.py # OpenAI + market forecast logic
├── forecast_history.csv # Saved forecasts & actuals
├── .env # API keys
└── README.md # This file


## 🚀 Getting Started

### 1. Clone the repo
git clone https://github.com/jugalsheth/geopulse-ai.git
cd geopulse-ai

2. Install dependencies
pip install -r requirements.txt

3. Set up API keys in .env
OPENAI_API_KEY=your_openai_key
NEWS_API_KEY=your_newsapi_key

4. Run it!
streamlit run app.py

🧪 Behind the Scenes — Our Journey

This project started as a bold question:
"Can we turn daily news into actionable market signals using GenAI?"

We iterated through:

Prompt engineering with OpenAI
Sentiment scoring techniques
Overlaying AI predictions with real S&P500 data
Accuracy scoring & cold-start tracking
Beautiful Plotly visualizations
What began as a learning experiment is now a working prototype.

🔮 What’s Next
Here’s what the next version of GeoPulse AI could include:

📆 Historical backtesting mode (load news & actuals for past dates)
🧠 Fine-tuned sentiment model for better context sensitivity
💼 Sector-specific forecasting (e.g., Energy, Tech)
⚙️ Scheduled daily automation with email alerts
☁️ Deploy to Streamlit Cloud / HuggingFace Spaces
💬 Slack/WhatsApp alerts based on thresholds

🤝 Contributing
This is an open exploration — if you're into NLP, LLMs, finance, or dashboards, feel free to fork, star, or suggest improvements!

👤 Author
Jugal Sheth
Data Engineer | AI Enthusiast | Builder of Useful Things
LinkedIn • GitHub
