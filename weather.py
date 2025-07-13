import requests

def get_weather(city="Chennai", api_key="38db43196275dd1e802f76d7730c7e60"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        return weather, temp
    except Exception:
        return "Unavailable", 0
