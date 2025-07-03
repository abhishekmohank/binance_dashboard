# 📊 Binance Crypto Market Dashboard

This project is a real-time cryptocurrency market tracker built using **Streamlit**, powered by **Binance's public API**. It displays the **top 10 traded coins** based on 24-hour volume and includes smart insights like **investment suggestions**, **market movement predictions**, and **trend charts** that update every 10 seconds.

---

## 🚀 Live Demo

⚠️ **IMPORTANT**: Due to **Binance's legal restrictions and regional API blocks**, this app may **not work correctly on Streamlit Cloud** (you may see a `451` error).  
✅ It works perfectly when run **locally** on your own machine. See instructions below.

---

## 🧠 Features

- ✅ **Top 10 Coins by 24h Volume**
- 🔄 **Auto-refresh every 10 seconds**
- 🔺 **Price Change with Emoji Indicators**
- 💡 **Market Suggestions** (Trending Up / Avoid / Neutral)
- 🔮 **Prediction Labels** (Likely ↑ / ↓ / Uncertain)
- 📈 **Trendline Charts** (Last 5 minutes of activity)
- 💵 **Currency Conversion Support**
  - Supports USD, INR, EUR, GBP, JPY
  - Uses live exchange rates via `exchangerate.host`
  - Falls back to manual rates if the API fails
- 🧭 **Sidebar Controls**:
  - Toggle Market Tips
  - Toggle Drop Alerts
  - Select preferred currency
- 🧠 Optimized with `@st.cache_data` for smooth refresh
- 🌐 Fully interactive via Streamlit UI

---

## 📦 Tech Stack

| Tool               | Purpose                            |
|--------------------|------------------------------------|
| `Streamlit`        | Web UI + real-time interactivity   |
| `Binance API`      | Live crypto market data            |
| `exchangerate.host`| Live USD-to-currency conversion    |
| `Pandas`           | Data processing and transformation |
| `Matplotlib`       | Price trend visualization          |
| `Requests`         | REST API access                    |

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

## 🛑 Known Issues

> Binance may **block Streamlit Cloud or other hosts** in certain regions, resulting in:
> ```
> 451 Client Error: Unavailable For Legal Reasons
> ```
> ✅ This app works fine on:
> - Your **local machine**
> - Platforms like **Render**, **Replit**, or **a personal VPS**

---

## ✅ Updates & Enhancements

- ✅ Market tip system showing top trending coins
- ✅ Drop alert system warning against falling assets
- ✅ Live currency conversion with USD, INR, EUR, GBP, JPY
- ✅ Fallback to manual conversion if API fails
- ✅ Smart emoji-based prediction and suggestions
- ✅ Live trend charting using Matplotlib
- ✅ Sidebar toggles and currency selector

---

## 🧪 Future Enhancements (Optional Ideas)

- 📤 Export table to CSV or JSON
- 📱 Make layout responsive on mobile
- 🔔 Add custom alerts (e.g., if price > X)
- 🧠 Basic ML for short-term trend prediction

---

## 🙋‍♂️ About the Author

Made with ❤️ by **Abhishek Mohan**  
🔗 [GitHub](https://github.com/abhishekmohank)  
🌐 [Portfolio](https://abhishek-amk.vercel.app)

---

## 📜 License

MIT License — free to use, modify, and share.
