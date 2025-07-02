import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta, date

# Load and preprocess
df = pd.read_csv('practice_trade.csv')
df['datetime'] = pd.to_datetime(df['TRANSACTION DATE/TIME'], format='%m/%d/%Y %I:%M:%S %p')
df['date'] = df['datetime'].dt.date

# Aggregate daily PnL and trade count
daily_summary = df.groupby('date').agg(
    total_pnl=('PNL', 'sum'),
    trade_count=('PNL', 'count')
).reset_index()

# Ask user for a month and year
st.title("📅 Monthly Trade Calendar")

today = datetime.today()
selected_month = st.selectbox("Select Month", range(1, 13), index=today.month - 1)
selected_year = st.selectbox("Select Year", range(2025, today.year + 1), index=today.year-2025)

# Calendar Generation
cal = calendar.Calendar(firstweekday=6)
month_days=cal.monthdatescalendar(selected_year, selected_month)

st.subheader(f"{calendar.month_name[selected_month]} {selected_year}")

# Build the calendar grid
weekday_headers = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
st.columns([1]*7)
header_cols = st.columns(7)

for i, day_name in enumerate(weekday_headers):
    header_cols[i].markdown(f"**{day_name}**")

for week in month_days:
    cols = st.columns(7)
    for i, day in enumerate(week):
        # Only show days in current week
        if day.month != selected_month:
            cols[i].markdown(" ")
            continue
        
        # Lookup PnL and trade count
        entry = daily_summary[daily_summary['date'] == day]
        if not entry.empty:
            pnl = entry.iloc[0]['total_pnl']
            trade_count = int(entry.iloc[0]['trade_count'])
            color = "#d4edda" if pnl > 0 else "#f8d7da"
            text_color = "#155724" if pnl > 0 else "#721c24"

            # Render cell
            cols[i].markdown(
                f"""
                <div style='background-color:{color};padding:8px;border-radius:5px;margin:5px;text-align:center;'>
                    <span style='color:black;font-weight:medium'>{day.day}</span><br>
                    <span style='color:{text_color};font-size:14px;font-weight:bolder;'>${abs(pnl):.0f}</span><br>
                    <span style='font-size:12px;color:#334155'>{trade_count} trade(s)</span>
                </div>
                """, unsafe_allow_html=True
            )

        else:
            cols[i].markdown(
                f"<div style='padding:8px;color:#888;text-align:center;margin:5px;vertical-align:middle;'>{day.day}</div>",
                unsafe_allow_html=True
            )