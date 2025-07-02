# 📊 Binance Crypto Market Dashboard

This project is a real-time cryptocurrency market tracker built using **Streamlit**, powered by **Binance's public API**. It displays the **top 10 traded coins** based on 24-hour volume and includes smart insights like **investment suggestions**, **market movement predictions**, and **trend charts** that update every 10 seconds.

---

## 🚀 Live Demo

⚠️ **IMPORTANT**: Due to **Binance's legal restrictions and regional API blocks**, this app may **not work correctly on Streamlit Cloud** (you may see a `451` error).  
✅ It works perfectly when run **locally** on your own machine. See instructions below.

---

## 🧠 Features

- ✅ **Top 10 Coins by 24h Volume**
- 📈 **Live Price Updates** (every 10 seconds)
- 🔺 **Price Change with Emoji Indicators**
- 💡 **Smart Suggestions**:
  - Trending Up
  - Falling
  - Neutral
- 🔮 **Movement Prediction** (based on price % change)
- 📊 **Price Trend Graphs** for each coin (last 5 minutes)
- 💵 **Formatted Price & Volume with $**
- 🧠 Optimized with `@st.cache_data` for smooth refresh

---

## 📦 Tech Stack

| Tool        | Purpose                           |
|-------------|-----------------------------------|
| `Streamlit` | Web UI + real-time interactivity  |
| `Binance API` | Live crypto market data        |
| `Pandas`    | Data processing and transformation|
| `Matplotlib`| Price trend visualization         |
| `Requests`  | REST API access                   |

---

## ⚙️ How to Run Locally

If the online version fails (due to Binance API block), run the app locally:

1. **Clone the repository**
   ```bash
   git clone https://github.com/abhishekmohank/binance_dashboard.git
   cd binance_dashboard
   ```

2. **Install the required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the app**
   ```bash
   streamlit run app.py
   ```

---

## 🛑 Known Issue (Streamlit Cloud & Binance)

> Binance occasionally **blocks traffic from certain cloud hosting providers** including **Streamlit Cloud**, causing the app to fail with:
> ```
> 451 Client Error: Unavailable For Legal Reasons
> ```
> This is outside of the app’s control. If this happens:
> - ✅ Run it **locally** (works perfectly)
> - ✅ Or deploy on another platform like **Render**, **Replit**, or a **VPS**

---

## 🧪 Coming Features (Optional Ideas)

- 🌍 Currency conversion (USD, INR, EUR, etc.)
- 🔔 Threshold-based price alerts
- 📤 Export top 10 data to CSV
- 📱 Responsive design for mobile

---

## 🙋‍♂️ About the Author

Made with ❤️ by **Abhishek Mohan**  
📍 [GitHub](https://github.com/abhishekmohank)

---

## 📜 License

MIT License — free to use, modify, and share.
