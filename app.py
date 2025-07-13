import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from logic import load_data, analyze_stock
from weather import get_weather, get_forecast

st.set_page_config(page_title="NeuroStock", layout="wide")

st.title("🧠 NeuroStock Dashboard")
st.markdown("### Smart discounting & restocking assistant for fresh inventory")

# ── WEATHER ───────────────────────────────────────────────
weather_desc, temp = get_weather()
forecast = get_forecast(7)

# ── LOAD INVENTORY DATA ───────────────────────────────────
df = load_data("data/data.csv")  # ← move this here

# Now it's safe to use df below
discount_df, restock_df = analyze_stock(df)


# ── WEATHER FORECAST ──────────────────────────────────────
st.markdown("---")
st.subheader("📆 7-Day Weather Forecast")

try:
    weather_table = pd.DataFrame(forecast)
    weather_table.rename(columns={"date": "📅 Date", "weather": "🌤️ Weather", "temp": "🌡️ Temp (°C)"}, inplace=True)
    st.table(weather_table)
    weather_descs = [d.get("weather", "") for d in forecast]
except Exception as e:
    st.warning("Forecast data unavailable.")

# ── Context-Aware Suggestions ─────────────────────────────
st.markdown("### 🔎 AI-Powered Recommendations")

weather_summary = " ".join([str(d.get("weather", "")).lower() for d in forecast])
recommendation_given = False

if "rain" in weather_summary:
    st.warning("🌧️ Rain detected! Boost promotion of hot foods like noodles, soups, and snacks.")
    recommendation_given = True
    if "noodle" in df["product_name"].str.lower().any():
        st.markdown("- Recommend offering **combo packs** with hot beverages.")
elif "clear" in weather_summary:
    st.info("☀️ Clear skies — Push cold items like juices, yogurt, and ice cream.")
    recommendation_given = True
elif "cloud" in weather_summary or "overcast" in weather_summary:
    st.info("⛅ Cloudy skies — Neutral impact, but monitor **dairy freshness** and **baked goods**.")
    recommendation_given = True
elif "snow" in weather_summary:
    st.warning("❄️ Cold weather — Ensure **soups and high-calorie items** are well stocked.")
    recommendation_given = True

# Default suggestion if nothing matched
if not recommendation_given:
    st.info("🧠 AI suggests monitoring fast-selling items and adjusting prices dynamically.")


# ── SIDEBAR: CATEGORY PIE CHART ───────────────────────────
st.sidebar.header("🗂️ Product Category Mix")
cat_count = df["category"].value_counts()
fig, ax = plt.subplots()
ax.pie(cat_count.values, labels=cat_count.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.sidebar.pyplot(fig)

# ── EXPIRY SEVERITY & DISCOUNTS ──────────────────────────
st.markdown("---")
st.subheader("📉 Suggested Discounts (with Severity)")

if not discount_df.empty:
    st.markdown(f"💡 **{len(discount_df)} items** may expire soon. Apply markdowns to reduce waste.")
    
    def get_severity_color(days):
        if days <= 1:
            return "🔴 Critical"
        elif days <= 3:
            return "🟠 Moderate"
        else:
            return "🟢 Low"

    discount_df["Severity"] = discount_df["expiry_days"].apply(get_severity_color)
    discount_df_sorted = discount_df.sort_values("expiry_days")

    st.dataframe(discount_df_sorted[["product_name", "category", "expiry_days", "price", "Severity"]])
else:
    st.success("🎉 No discounts needed today!")

# ── RESTOCK SECTION ───────────────────────────────────────
st.subheader("🚨 Restock Alerts")

if not restock_df.empty:
    st.markdown(f"⚠️ **{len(restock_df)} items** need urgent replenishment.")
    st.dataframe(restock_df[["product_name", "category", "stock_left", "daily_sales"]])
else:
    st.success("✅ Stock levels are stable!")

# ── EXPANDABLE RAW DATA ───────────────────────────────────
with st.expander("🔍 Show Raw Inventory Data"):
    st.dataframe(df)
