import tkinter as tk
import requests

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == 200:
        weather_data = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
        return weather_data
    else:
        return None

def get_weather_for_city():
    city = city_entry.get()
    api_key = api_key_entry.get()
    if not city:
        result_label.config(text="Please enter a city name.")
        return
    if not api_key:
        result_label.config(text="Please enter an API key.")
        return

    weather = get_weather(city, api_key)
    
    if weather:
        result_label.config(text=f"Temperature: {weather['temperature']}°C\nHumidity: {weather['humidity']}%\nDescription: {weather['description']}")
    else:
        result_label.config(text="City not found. Please check the spelling or try another API key.")

root = tk.Tk()
root.title("Weather App")

tk.Label(root, text="Enter city name:").pack()
city_entry = tk.Entry(root)
city_entry.pack()

tk.Label(root, text="Enter API key:").pack()
api_key_entry = tk.Entry(root)
api_key_entry.pack()

result_label = tk.Label(root, text="")
result_label.pack()

get_weather_button = tk.Button(root, text="Get Weather", command=get_weather_for_city)
get_weather_button.pack()
