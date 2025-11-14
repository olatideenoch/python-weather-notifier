import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

OWM_Endpoint = os.getenv("OWM_ENDPOINT")
api_key = os.getenv("API_KEY")  
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
my_twilio_num = os.getenv("MY_TWILIO_NUM")
my_num = os.getenv("MY_NUM")

weather_params = {
    "lat": 7.641729,
    "lon": 5.240347,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()  
weather_data = response.json()
print(weather_data["list"][0]["weather"][0]["id"])

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True
        break

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella ☔",
        from_=my_twilio_num,
        to=my_num,
    )
    print(message.status)
else:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's not going to rain today. Enjoy your day! ☀️",
        from_=my_twilio_num,
        to=my_num,
    )
    print(message.status)

        