import requests

API_KEY = "38db43196275dd1e802f76d7730c7e60"
LOCATION = "Chennai"

def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()
        description = res["weather"][0]["main"]
        temp = round(res["main"]["temp"])
        return description, temp
    except:
        return "Unavailable", "--"

def get_forecast(days=3):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={LOCATION}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()
        forecasts = [res["list"][i*8]["weather"][0]["main"] for i in range(days)]
        return forecasts
    except:
        return ["Unavailable"] * days
