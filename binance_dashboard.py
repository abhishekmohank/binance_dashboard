import streamlit as st
import pandas as pd
import requests
import time
import matplotlib.pyplot as plt

# Streamlit config
st.set_page_config(page_title="Binance Crypto Tracker", layout="wide")
st.title("📊 Binance Crypto Market Dashboard")
st.caption("Updates every 10 seconds. Shows live top 10 coins by 24h volume.")

@st.cache_data(ttl=10)
def fetch_market_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list):
            st.error("⚠️ Binance API returned unexpected data format.")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df = df[["symbol", "lastPrice", "priceChangePercent", "quoteVolume"]]
        df["quoteVolume"] = df["quoteVolume"].astype(float)
        df["priceChangePercent"] = df["priceChangePercent"].astype(float)
        df["lastPrice"] = df["lastPrice"].astype(float)
        return df.sort_values("quoteVolume", ascending=False).head(10)

    except Exception as e:
        st.error(f"❌ Error fetching data from Binance API:\n\n{e}")
        return pd.DataFrame()

def format_change(pct):
    return f"🔺 {pct:.2f}%" if pct > 0 else f"🔻 {pct:.2f}%"

def suggest_investment(row):
    if row["priceChangePercent"] > 2 and row["quoteVolume"] > 100_000_000:
        return "✅ Suggest: Trending Up"
    elif row["priceChangePercent"] < -3:
        return "⚠️ Avoid: Falling"
    else:
        return "➖ Neutral"

def predict_movement(row):
    if row["priceChangePercent"] > 3:
        return "📈 Likely ↑"
    elif row["priceChangePercent"] < -3:
        return "📉 Likely ↓"
    else:
        return "❓ Uncertain"

# Track price history
if "history" not in st.session_state:
    st.session_state.history = {}

# Fetch data
df = fetch_market_data()

# Only proceed if we have data
if not df.empty:
    df["Change (24h)"] = df["priceChangePercent"].apply(format_change)
    df["Suggestion"] = df.apply(suggest_investment, axis=1)
    df["Prediction"] = df.apply(predict_movement, axis=1)

    # 💡 Market Tip section
    rising_coins = df[df["Prediction"] == "📈 Likely ↑"]
    if not rising_coins.empty:
        suggested = ", ".join(rising_coins["symbol"].tolist())
        st.success(f"💡 **Market Tip**: You may consider watching or buying: **{suggested}** — these coins are showing upward momentum.")
    else:
        st.info("🔎 No strong upward trends detected at the moment.")

    # Format price and volume with $
    df["Last Price (USDT)"] = df["lastPrice"].apply(lambda x: f"${x:,.2f}")
    df["24h Volume (USDT)"] = df["quoteVolume"].apply(lambda x: f"${x:,.0f}")

    # Update session history
    for _, row in df.iterrows():
        symbol = row["symbol"]
        price = row["lastPrice"]
        if symbol not in st.session_state.history:
            st.session_state.history[symbol] = []
        st.session_state.history[symbol].append(price)
        st.session_state.history[symbol] = st.session_state.history[symbol][-30:]

    # Display table
    st.subheader("📋 Top 10 Coins by Volume")
    st.dataframe(
        df[["symbol", "Last Price (USDT)", "Change (24h)", "Suggestion", "Prediction", "24h Volume (USDT)"]]
          .rename(columns={"symbol": "Symbol"}),
        use_container_width=True,
        hide_index=True
    )

    # Display charts
    st.subheader("📈 Price Trend Charts (Last 5 minutes, 10s intervals)")

    cols = st.columns(2)
    for i, (symbol, prices) in enumerate(list(st.session_state.history.items())[:6]):
        with cols[i % 2]:
            st.markdown(f"**{symbol}**")
            fig, ax = plt.subplots()
            ax.plot(prices, marker='o')
            ax.set_title(f"{symbol} Price Trend")
            ax.set_xlabel("Ticks (10s interval)")
            ax.set_ylabel("Price (USDT)")
            ax.grid(True)
            st.pyplot(fig)
else:
    st.warning("🔄 Waiting for valid data from Binance API...")
