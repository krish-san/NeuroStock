# backend/app/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .logic import analyze_stock, load_data
from .weather import get_weather, get_forecast

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow everything for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Fix this absolute path to data.csv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # /home/.../backend/app
CSV_PATH = os.path.join(BASE_DIR, "data", "data.csv")  # /home/.../backend/app/data/data.csv


@app.get("/weather/current")
def current_weather():
    desc, temp = get_weather()
    return {"description": desc, "temperature": temp}

@app.get("/weather/forecast")
def forecast_weather():
    return get_forecast(7)

@app.get("/inventory/discounts")
def discount_data():
    df = load_data(CSV_PATH)
    discount_df, _ = analyze_stock(df)
    return discount_df.to_dict(orient="records")

@app.get("/inventory/restock")
def restock_data():
    df = load_data(CSV_PATH)
    _, restock_df = analyze_stock(df)
    return restock_df.to_dict(orient="records")

@app.get("/dashboard-data")
def dashboard_data():
    df = load_data(CSV_PATH)
    discount_df, restock_df = analyze_stock(df)
    return {
        "discounts": discount_df.to_dict(orient="records"),
        "restocks": restock_df.to_dict(orient="records")
    }
