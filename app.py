import streamlit as st
import pandas as pd
from logic import load_data, analyze_stock
from weather import get_weather
import matplotlib.pyplot as plt

st.set_page_config(page_title="NeuroStock", layout="wide")

st.title("🧠 NeuroStock Dashboard")
st.markdown("### Smart discounting & restocking assistant for fresh inventory")

# ── WEATHER ───────────────────────────────────────────────
weather_desc, temp = get_weather()
st.markdown("---")

col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("**📍 Weather Now**")
with col2:
    if weather_desc != "Unavailable":
        st.info(f"{weather_desc} | 🌡️ {temp}°C")
    else:
        st.error("Unable to fetch live weather. Check your API key or internet.")

# Weather-based demand hints
if "Rain" in weather_desc:
    st.warning("🌧️ Rainy weather — Consider stocking more soups, instant foods, and warm meals.")
elif "Clear" in weather_desc:
    st.info("☀️ Clear skies — Boost cold beverages, ice cream, and juices.")
elif "Cloud" in weather_desc:
    st.info("⛅ Cloudy day — Neutral impact, but monitor fresh foods closely.")

st.markdown("---")

# ── LOAD INVENTORY DATA ───────────────────────────────────
df = load_data("data/data.csv")
discount_df, restock_df = analyze_stock(df)

# ── SIDEBAR: CATEGORY BREAKDOWN ───────────────────────────
st.sidebar.header("🗂️ Product Category Mix")
cat_count = df["category"].value_counts()

fig, ax = plt.subplots()
ax.pie(cat_count.values, labels=cat_count.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.sidebar.pyplot(fig)

# ── DISCOUNT SECTION ──────────────────────────────────────
st.subheader("📉 Suggested Discounts")
if not discount_df.empty:
    st.markdown(f"**💡 {len(discount_df)} items may expire soon. Apply markdowns to avoid waste.**")
    st.dataframe(discount_df)
else:
    st.success("🎉 No items need discounting today!")

# ── RESTOCK SECTION ───────────────────────────────────────
st.subheader("🚨 Restock Alerts")
if not restock_df.empty:
    st.markdown(f"**⚠️ {len(restock_df)} items are at risk of going out of stock. Consider replenishment.**")
    st.dataframe(restock_df)
else:
    st.success("✅ Stock levels look healthy across inventory!")

# ── EXPANDABLE RAW DATA ───────────────────────────────────
with st.expander("🔍 Show Raw Inventory Data"):
    st.dataframe(df)


