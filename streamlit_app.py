import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Futures Trade Calendar", layout="wide")

# Load CSV
@st.cache_data
def load_data():
    df = pd.read_csv("practice_trade.csv")
    df['datetime'] = pd.to_datetime(df["TRANSACTION DATE/TIME"], format="%m/%d/%Y %I:%M:%S %p")
    df["date"] = df["datetime"].dt.date
    return df

df = load_data()

# Create Daily Summary
daily_summary = df.groupby('date').agg(
    total_pnl=('PNL', 'sum'),
    trade_count=('PNL', 'count')
).reset_index()

# Show daily summary as a table with color cue
st.subheader("Daily Performance Summary")
for _, row in daily_summary.iterrows():
    color = "#0E6E24" if row['total_pnl'] > 0 else "#d62f3d"
    st.markdown(
        f"<div style='background:{color}; padding:10px; border-radius:5px; margin-bottom:5px;'>"
        f"<b>{row['date']}</b> - PnL: ${row['total_pnl']} | Trades: {row['trade_count']}</div>",
        unsafe_allow_html=True
    )