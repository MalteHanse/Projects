import requests
from twilio.rest import Client
import os 
from dotenv import load_dotenv
load_dotenv()


# weather API
API_KEY = os.getenv("API_KEY")
CITY = "Aarhus"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# twilio API
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
FROM_NUMBER = os.getenv("FROM_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER")

def fetch_weather(URL):
    response = requests.get(URL)
    data = response.json()
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]
    wind = data["wind"]["speed"]
    weather = {"description": description, "temp":temperature, "wind":wind}
    return weather

def format_message(weather):
    temperature = weather["temp"]
    wind = weather["wind"]
    description = weather["description"]

    message = f"Good morning! Current weather: {temperature}°C, {description}. Wind: {wind}m/s"
    return message

def send_message(message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    sms = client.messages.create(
        body=message,
        from_=FROM_NUMBER,
        to=TO_NUMBER
    )

send_message(format_message(fetch_weather(URL)))