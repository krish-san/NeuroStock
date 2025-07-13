import os
import requests
from datetime import datetime

# Either use environment variable or hardcode your API key here:
API_KEY = os.getenv("38db43196275dd1e802f76d7730c7e60")
CITY = "Chennai"
URL = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

def get_weather():
    try:
        response = requests.get(URL)
        data = response.json()
        weather_description = data["list"][0]["weather"][0]["description"].title()
        temperature = round(data["list"][0]["main"]["temp"])
        return weather_description, temperature
    except:
        return "Unavailable", 0

def get_forecast(days=5):
    try:
        response = requests.get(URL)
        data = response.json()

        seen_dates = set()
        forecast_data = []

        for entry in data["list"]:
            date_str = entry["dt_txt"].split(" ")[0]
            if date_str not in seen_dates:
                seen_dates.add(date_str)

                day_name = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
                weather_description = entry["weather"][0]["description"].title()
                temperature = round(entry["main"]["temp"])

                forecast_data.append({
                    "day": day_name,
                    "description": weather_description,
                    "temperature": temperature
                })

                if len(forecast_data) == days:
                    break

        return forecast_data

    except Exception as e:
        return [{"day": "N/A", "description": "Unavailable", "temperature": 0}]
