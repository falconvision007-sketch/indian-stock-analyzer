import streamlit as st
import yfinance as yf
import pandas as pd
import time

# ====================== PASSWORD PROTECTION ======================
st.set_page_config(page_title="Falcon's Analyzer", layout="wide", page_icon="📊")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login to Falcon's Stock Analyzer")
    st.markdown("### Enter your password")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if password == "falcon2026":   # ← CHANGE THIS TO YOUR OWN PASSWORD
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Incorrect password")

if not st.session_state.logged_in:
    login()
    st.stop()
# ====================== END PASSWORD ======================

# Light theme
st.markdown("""
<style>
    .main {background-color: #f8fafc;}
    .card {background-color: #ffffff; border-radius: 16px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border: 1px solid #e2e8f0;}
    h1, h2, h3 {color: #0f172a;}
    .positive {color: #10b981;}
    .negative {color: #ef4444;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Falcon's Indian Stock Fundamental Analyzer")
st.caption("Personal Use Only • Live Data • cryptorank.io Light Theme")

page = st.sidebar.selectbox("Choose Section", 
    ["🏠 Home - Macro Dashboard", "Single Stock Analysis", "🕌 Zamzam Halal Stocks"])

auto_refresh = st.sidebar.checkbox("🔄 Enable Auto-Refresh every 60s", value=False)

# Halal List
BASE_HALAL_TICKERS = ["BHARTIARTL", "HINDUNILVR", "SUNPHARMA", "ULTRACEMCO", "ONGC", "COALINDIA", "NESTLEIND", "ASIANPAINT", "ITC", "MARUTI", "LT", "RELIANCE", "ICICIBANK", "SBIN", "KOTAKBANK", "AXISBANK", "INFY", "TCS", "HCLTECH", "TATAMOTORS", "AVENUE", "DMART", "HAL", "TITAN", "DIVISLAB", "WIPRO"]

if 'custom_halal' not in st.session_state:
    st.session_state.custom_halal = []

# ==================== HOME DASHBOARD ====================
if page == "🏠 Home - Macro Dashboard":
    st.markdown("<h2 style='text-align:center;'>📈 Global Macro Dashboard</h2>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown('<div class="card"><strong>S&P 500</strong><br><h3>$7,126</h3><span class="positive">+1.20%</span></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="card"><strong>Nasdaq-100</strong><br><h3>26,672</h3><span class="positive">+1.29%</span></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="card"><strong>Dow Jones</strong><br><h3>48,579</h3><span class="positive">+0.36%</span></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="card"><strong>VIX</strong><br><h3>18.45</h3><span class="negative">-2.1%</span></div>', unsafe_allow_html=True)
    with c5: st.markdown('<div class="card"><strong>BTC (USD)</strong><br><h3>$74,786</h3><span class="positive">+0.64%</span></div>', unsafe_allow_html=True)

# ==================== ZAMZAM HALAL STOCKS ====================
elif page == "🕌 Zamzam Halal Stocks":
    st.subheader("🕌 Zamzam Halal Stocks - Live Dashboard")

    pasted = st.text_area("Paste latest Zamzam Halal tickers (one per line)", height=120, placeholder="TANLA\nRELIANCE\n...")
    if st.button("Load/Update Custom List"):
        if pasted:
            new_list = [t.strip().upper() for t in pasted.replace(",", "\n").splitlines() if t.strip()]
            st.session_state.custom_halal = list(set(new_list))
            st.success(f"Loaded {len(new_list)} stocks!")

    if st.button("🔄 Refresh All Halal Data"):
        st.rerun()

    tickers = BASE_HALAL_TICKERS + st.session_state.custom_halal
    results = []

    with st.spinner("Fetching latest data..."):
        for t in tickers:
            try:
                s = yf.Ticker(t + ".NS")
                info = s.info
                eps = info.get('trailingEps', 0)
                intrinsic = eps * 25.9 if eps else 0
                price = info.get('currentPrice', 0)
                margin = ((intrinsic - price) / price * 100) if price > 0 else 0

                results.append({
                    "Stock Name": info.get('longName', t),
                    "Price": round(price, 2),
                    "52 Week Low": round(info.get('fiftyTwoWeekLow', 0), 2),
                    "52 Week High": round(info.get('fiftyTwoWeekHigh', 0), 2),
                    "Intrinsic Value": round(intrinsic, 2),
                    "% Over/Undervalued": round(margin, 2),
                    "PE": round(info.get('trailingPE', 0), 2),
                    "PB": round(info.get('priceToBook', 0), 2),
                })
            except:
                pass

    if results:
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Click Refresh to load data")

else:
    st.info("Select a section from the sidebar.")

if auto_refresh:
    time.sleep(60)
    st.rerun()
