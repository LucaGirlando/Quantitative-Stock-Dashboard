import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import numpy as np

# Configurazione
st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.markdown("""<div style='text-align: center; font-size:18px;'>Created by: <a href="https://www.linkedin.com/in/luca-girlando-775463302/" target="_blank">Luca Girlando</a></div><br>""", unsafe_allow_html=True)
st.title("📊 Quantitative Stock Dashboard")

# Custom CSS for styling
st.markdown("""
<style>
:root {
    --primary-dark: #1a2639;
    --primary-medium: #3e4a61;
    --primary-light: #d9dad7;
    --accent-blue: #4a6fa5;
    --accent-teal: #166088;
    --call-green: #2e8b57;
    --put-red: #c04e4e;
    --highlight: #f0f4f8;
}

* {
    font-family: 'Lato', 'Segoe UI', Roboto, sans-serif;
}

html, body, .stApp {
    background-color: #f8f9fa;
}

h1, h2, h3, h4 {
    color: var(--primary-dark);
    font-weight: 700;
    letter-spacing: -0.015em;
}

.stSidebar {
    background: linear-gradient(135deg, var(--primary-dark), var(--primary-medium)) !important;
    color: white !important;
}

.stSidebar label {
    color: white !important;
    font-weight: 500 !important;
}

.metric-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 1.8rem 2rem;
    border-radius: 12px;
    background: white;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
    text-align: center;
    border: 1px solid rgba(0,0,0,0.05);
    transition: all 0.3s ease-in-out;
}

.metric-container:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.1);
}

.metric-value {
    font-size: 2.1rem;
    font-weight: 800;
    font-family: 'Roboto Mono', monospace;
    margin: 0.7rem 0;
    color: var(--primary-dark);
}

.metric-label {
    font-size: 1.05rem;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--primary-medium);
    margin-bottom: 0.5rem;
}

.stDataFrame {
    border-radius: 10px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    border: 1px solid rgba(0,0,0,0.03) !important;
}

.footer {
    font-size: 0.78rem;
    text-align: center;
    margin-top: 3rem;
    color: #6c757d;
    padding: 1.2rem;
    border-top: 1px solid #e9ecef;
    letter-spacing: 0.03em;
}
</style>
""", unsafe_allow_html=True)

# Sidebar input
st.sidebar.header("Input")
ticker_symbol = st.sidebar.text_input("Ticker Symbol (e.g. AAPL, MSFT, TSLA):", "AAPL")
start_date = st.sidebar.date_input("Start Date", datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

ticker = yf.Ticker(ticker_symbol)
hist = ticker.history(start=start_date, end=end_date)

# Header
st.header(f"📈 {ticker_symbol} Stock Overview")

# Company Info
info = ticker.info
col1, col2 = st.columns(2)
with col1:
    st.subheader("🏢 Company Profile")
    st.write(f"**Name:** {info.get('longName', 'N/A')}")
    st.write(f"**Sector:** {info.get('sector', 'N/A')}")
    st.write(f"**Industry:** {info.get('industry', 'N/A')}")
    st.write(f"**Country:** {info.get('country', 'N/A')}")
    st.write(f"**Website:** [{info.get('website', 'N/A')}]({info.get('website', '')})")
    st.write(f"**Employees:** {info.get('fullTimeEmployees', 'N/A')}")

with col2:
    st.subheader("📊 Valuation Metrics")
    st.write(f"**Market Cap:** {info.get('marketCap', 'N/A'):,}")
    st.write(f"**Trailing P/E:** {info.get('trailingPE', 'N/A')}")
    st.write(f"**Forward P/E:** {info.get('forwardPE', 'N/A')}")
    st.write(f"**PEG Ratio:** {info.get('pegRatio', 'N/A')}")
    st.write(f"**Price to Book:** {info.get('priceToBook', 'N/A')}")
    st.write(f"**ROE:** {info.get('returnOnEquity', 'N/A'):.2%}" if info.get("returnOnEquity") else "N/A")

# Price Chart
st.subheader("📈 Price History")
st.line_chart(hist["Close"])

# Technical Analysis
st.subheader("📐 Technical Indicators")
hist["SMA20"] = hist["Close"].rolling(window=20).mean()
hist["SMA50"] = hist["Close"].rolling(window=50).mean()
hist["Daily Return"] = hist["Close"].pct_change()
hist["Volatility"] = hist["Daily Return"].rolling(window=20).std()

st.line_chart(hist[["Close", "SMA20", "SMA50"]])

col3, col4 = st.columns(2)
with col3:
    st.metric("📊 Volatility (20d STD)", f"{hist['Volatility'].iloc[-1]:.2%}")
    st.metric("📉 Max Daily Loss", f"{hist['Daily Return'].min():.2%}")
with col4:
    st.metric("📈 Max Daily Gain", f"{hist['Daily Return'].max():.2%}")
    st.metric("📆 Mean Daily Return", f"{hist['Daily Return'].mean():.2%}")

# Returns
st.subheader("📅 Returns Summary")
returns = pd.DataFrame()
returns["Daily"] = hist["Close"].pct_change()
returns["Monthly"] = hist["Close"].resample("M").ffill().pct_change()
returns["Yearly"] = hist["Close"].resample("Y").ffill().pct_change()

col5, col6, col7 = st.columns(3)
col5.metric("📈 Daily Return Mean", f"{returns['Daily'].mean():.2%}")
col6.metric("📅 Monthly Return Mean", f"{returns['Monthly'].mean():.2%}")
col7.metric("📆 Yearly Return Mean", f"{returns['Yearly'].mean():.2%}")

# Financials
st.header("📄 Financial Statements")
with st.expander("📊 Income Statement"):
    st.dataframe(ticker.financials)
with st.expander("📋 Balance Sheet"):
    st.dataframe(ticker.balance_sheet)
with st.expander("💵 Cash Flow"):
    st.dataframe(ticker.cashflow)

# Earnings
st.header("💰 Earnings")
st.subheader("Annual Earnings")
st.dataframe(ticker.earnings)
st.subheader("Quarterly Earnings")
st.dataframe(ticker.quarterly_earnings)

# Dividends & Splits
st.header("📆 Dividends & Stock Splits")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Dividends")
    st.line_chart(ticker.dividends)
with col2:
    st.subheader("Splits")
    st.dataframe(ticker.splits)

# Ownership & Insider Trading
st.header("🏦 Ownership & Insider Trading")
with st.expander("📌 Institutional Holders"):
    st.dataframe(ticker.institutional_holders)
with st.expander("👤 Major Holders"):
    st.dataframe(ticker.major_holders)
with st.expander("🔒 Insider Transactions"):
    st.dataframe(ticker.insider_transactions)

# Analyst Recommendations
st.header("🧠 Analyst Recommendations")
with st.expander("⭐ Ratings Over Time"):
    st.dataframe(ticker.recommendations)

# ESG Scores
st.header("🌱 ESG & Sustainability")
st.dataframe(ticker.sustainability)

# Options Data
st.header("📈 Options Data")
option_dates = ticker.options
if option_dates:
    selected_date = st.selectbox("Select Expiration Date", option_dates)
    option_chain = ticker.option_chain(selected_date)
    st.subheader("Calls")
    st.dataframe(option_chain.calls)
    st.subheader("Puts")
    st.dataframe(option_chain.puts)
else:
    st.warning("No options data available for this ticker.")

# Calendar Events
st.header("📅 Events & Calendar")
st.dataframe(ticker.calendar)

# Footer
st.markdown("""<br><div style='text-align: center; font-size:18px;'>Created by: <a href="https://www.linkedin.com/in/luca-girlando-775463302/" target="_blank">Luca Girlando</a></div>""", unsafe_allow_html=True)
