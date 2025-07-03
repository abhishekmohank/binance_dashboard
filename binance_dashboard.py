import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Binance Crypto Tracker", layout="wide")
st.title("📊 Binance Crypto Market Dashboard")

# 🔁 Auto-refresh every 10 seconds
st_autorefresh(interval=10 * 1000, limit=None, key="auto_refresh")

st.caption("Updates every 10 seconds. Shows live top 10 coins by 24h volume.")

# Currency symbols
currency_symbols = {
    "USD": "$",
    "INR": "₹",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥"
}

# Hybrid exchange rate: live + fallback
def get_exchange_rate(to_currency):
    manual_rates = {
        "USD": 1,
        "INR": 83.2,
        "EUR": 0.92,
        "GBP": 0.78,
        "JPY": 157.6
    }

    if to_currency == "USD":
        return 1

    try:
        url = f"https://api.exchangerate.host/latest?base=USD&symbols={to_currency}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not data.get("success") or to_currency not in data.get("rates", {}):
            raise ValueError("Invalid exchange rate response.")

        return data["rates"][to_currency]
    except Exception as e:
        st.warning(f"⚠️ Could not fetch live rate for {to_currency}. Using fallback.\n\nError: {e}")
        return manual_rates.get(to_currency, 1)

# Fetch Binance market data
@st.cache_data(ttl=10)
def fetch_market_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            st.error("⚠️ Binance API returned unexpected format.")
            return pd.DataFrame()
        df = pd.DataFrame(data)
        df = df[["symbol", "lastPrice", "priceChangePercent", "quoteVolume"]]
        df["quoteVolume"] = df["quoteVolume"].astype(float)
        df["priceChangePercent"] = df["priceChangePercent"].astype(float)
        df["lastPrice"] = df["lastPrice"].astype(float)
        return df.sort_values("quoteVolume", ascending=False).head(10)
    except Exception as e:
        st.error(f"❌ Error fetching Binance data: {e}")
        return pd.DataFrame()

# Helpers
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

# Sidebar
st.sidebar.header("🔧 Options")
show_market_tip = st.sidebar.checkbox("💡 Show Market Tip", True)
show_drop_alert = st.sidebar.checkbox("📉 Show Drop Alert", True)
st.sidebar.markdown("💱 **Currency Conversion**")
currency = st.sidebar.selectbox("Convert to:", ["USD", "INR", "EUR", "GBP", "JPY"], index=0)
exchange_rate = get_exchange_rate(currency)
currency_symbol = currency_symbols.get(currency, "$")
st.sidebar.caption("🔁 Uses live rates with fallback to manual.")

# Track chart history
if "history" not in st.session_state:
    st.session_state.history = {}

# Fetch data
df = fetch_market_data()

if not df.empty:
    df["Change (24h)"] = df["priceChangePercent"].apply(format_change)
    df["Suggestion"] = df.apply(suggest_investment, axis=1)
    df["Prediction"] = df.apply(predict_movement, axis=1)

    # Convert price/volume
    df["converted_price"] = df["lastPrice"] * exchange_rate
    df["converted_volume"] = df["quoteVolume"] * exchange_rate
    df["Last Price"] = df["converted_price"].apply(lambda x: f"{currency_symbol}{x:,.2f}")
    df["24h Volume"] = df["converted_volume"].apply(lambda x: f"{currency_symbol}{x:,.0f}")

    # Market tip
    if show_market_tip:
        rising = df[df["Prediction"] == "📈 Likely ↑"]
        if not rising.empty:
            coins = ", ".join(rising["symbol"].tolist())
            st.success(f"💡 **Market Tip**: Watch or buy: **{coins}** — trending up.")
        else:
            st.info("🔎 No strong upward trends right now.")

    # Drop alert
    if show_drop_alert:
        falling = df[df["Prediction"] == "📉 Likely ↓"]
        if not falling.empty:
            coins = ", ".join(falling["symbol"].tolist())
            st.warning(f"⚠️ **Drop Alert**: Falling coins: **{coins}**. Watch out.")
        else:
            st.info("✅ No sharp drops detected.")

    # Update chart history
    for _, row in df.iterrows():
        sym = row["symbol"]
        price = row["converted_price"]
        if sym not in st.session_state.history:
            st.session_state.history[sym] = []
        st.session_state.history[sym].append(price)
        st.session_state.history[sym] = st.session_state.history[sym][-30:]

    # Display table
    st.subheader(f"📋 Top 10 Coins by Volume ({currency})")
    st.dataframe(
        df[["symbol", "Last Price", "Change (24h)", "Suggestion", "Prediction", "24h Volume"]]
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
            ax.set_title(f"{symbol} Price Trend ({currency})")
            ax.set_xlabel("Ticks (10s)")
            ax.set_ylabel(f"Price ({currency_symbol})")
            ax.grid(True)
            st.pyplot(fig)
else:
    st.warning("🔄 Waiting for valid data from Binance API...")
