import streamlit as st
from news_fetcher import fetch_news
from sentiment_forecaster import analyze_sentiment, forecast_market, save_forecast
import pandas as pd
import plotly.graph_objects as go
import os
import datetime
import yfinance as yf

# --- Setup ---
st.set_page_config(page_title="GeoPulse AI", layout="wide")
if "actual_movement" not in st.session_state:
    st.session_state.actual_movement = None

st.title("🧠 GeoPulse AI — News Feed & Sentiment")

# --- User Input ---
query = st.text_input("Enter a news topic", "geopolitics")
days_back = st.slider("Days of S&P 500 History", min_value=7, max_value=60, value=30)

# --- News + Sentiment Analysis ---
if st.button("📰 Fetch News & Forecast"):
    news = fetch_news(query)
    st.write(f"### Found {len(news)} articles")

    for item in news:
        sentiment = analyze_sentiment(item["content"])
        st.subheader(item["title"])
        st.markdown(f"**Sentiment:** <span style='color:lime'>{sentiment}</span>", unsafe_allow_html=True)
        st.write(item["content"])
        st.markdown(f"[🔗 Read more]({item['url']})")

    forecast = forecast_market(news)
    st.success(forecast)

# --- Actual Market Movement ---
st.divider()
st.subheader("📉 Actual Market Movement")

if st.button("📉 Fetch Actual Movement from S&P 500"):
    today = datetime.date.today().isoformat()
    sp500 = yf.Ticker("^GSPC")
    data = sp500.history(period="7d")

    if len(data) >= 2:
        change = data["Close"].iloc[-1] - data["Close"].iloc[-2]
        actual_movement = "Bullish" if change > 0 else "Bearish" if change < 0 else "Neutral"
        st.session_state.actual_movement = actual_movement

        df = pd.read_csv("forecast_history.csv")
        if today in df["date"].values:
            df.loc[df["date"] == today, "actual"] = actual_movement
            df.to_csv("forecast_history.csv", index=False)
            st.success(f"✅ Actual market movement ({actual_movement}) updated.")

if st.session_state.actual_movement:
    st.info(f"📈 Today's actual market movement: **{st.session_state.actual_movement}**")

# --- Forecast Accuracy Section ---
st.divider()
st.subheader("📊 Forecast Accuracy")

def load_forecast_history():
    if not os.path.exists("forecast_history.csv"):
        return pd.DataFrame(columns=["date", "prediction", "actual"])
    return pd.read_csv("forecast_history.csv")

def get_sp500_history(days):
    ticker = yf.Ticker("^GSPC")
    hist = ticker.history(period=f"{days}d").reset_index()
    hist["date"] = pd.to_datetime(hist["Date"]).dt.date
    return hist[["date", "Close"]]

def merge_forecast_with_market(sp500_df, forecast_df):
    forecast_df["date"] = pd.to_datetime(forecast_df["date"]).dt.date
    sp500_df["date"] = pd.to_datetime(sp500_df["date"]).dt.date
    merged = sp500_df.merge(forecast_df, on="date", how="left")
    merged["match"] = merged["prediction"].str.lower() == merged["actual"].str.lower()
    return merged

def show_forecast_accuracy():
    df = load_forecast_history()
    if df.empty:
        st.warning("No forecast history available.")
        return

    df["date"] = pd.to_datetime(df["date"])
    df["prediction"] = df["prediction"].astype(str).str.strip().str.title()
    df["actual"] = df["actual"].astype(str).str.strip().str.title()
    df["match"] = df["prediction"] == df["actual"]

    sp500_df = get_sp500_history(days_back)
    merged = merge_forecast_with_market(sp500_df, df)

    # --- Forecast Accuracy Score ---
    correct = merged["match"].sum()
    total = merged["match"].count()
    accuracy = (correct / total) * 100 if total > 0 else 0
    st.metric("Forecast Accuracy", f"{accuracy:.2f}% ({correct}/{total})")
    st.progress(int(accuracy))

    # --- Interactive Plot ---
    st.subheader("📈 Unified Market Trend + Forecast Accuracy (Interactive)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=merged["date"], y=merged["Close"],
                             mode="lines+markers", name="S&P 500", line=dict(color="white")))

    for i, row in merged.iterrows():
        if pd.notna(row["prediction"]):
            color = dict(Bullish="green", Bearish="red", Neutral="gray").get(row["prediction"], "blue")
            fig.add_shape(type="rect",
                         x0=row["date"], x1=row["date"],
                         y0=min(merged["Close"]), y1=max(merged["Close"]),
                         line=dict(width=0), fillcolor=color, opacity=0.15, layer="below")

            fig.add_trace(go.Scatter(
                x=[row["date"]], y=[row["Close"]],
                mode="markers",
                marker=dict(color="green" if row["match"] else "red", size=10, symbol="circle"),
                name="Correct" if row["match"] else "Incorrect",
                showlegend=False
            ))

    fig.update_layout(template="plotly_dark", xaxis_title="Date", yaxis_title="S&P 500 Close")
    st.plotly_chart(fig, use_container_width=True)

    # --- Download Data ---
    st.download_button("📥 Export Combined Dataset", merged.to_csv(index=False), file_name="geo_forecast_data.csv")

show_forecast_accuracy()
