import requests

def weather(city):
    url = f'http://api.weatherapi.com/v1/current.json?key=6bab20eb12f642769cf184204252204&q={city}'
    response = requests.get(url)
    data = response.json()

    if data:
        location = data['location']['name']
        timezone = data['location']['tz_id']
        local_time = data['location']['localtime']
        temp_celsius = data['current']['temp_c']
        cloud_cover = data['current']['cloud']
        return location, timezone, local_time, temp_celsius, cloud_cover
    else:
        print('No data')
        return None

data = weather('New York')
cloud_cover = data[-1]


alert_message = f"Cloud cover is currently {cloud_cover}%. "

# Customize alert levels
if cloud_cover==0:
  print('No cloud coverage today')
if cloud_cover > 80:
    alert_message += "⚠️ High cloud cover — significant drop in solar output expected."
elif 50 < cloud_cover <= 80:
    alert_message += "☁️ Moderate cloud cover — slight reduction in solar efficiency."
else:
    alert_message += "☀️ Low cloud cover — good conditions for solar generation."