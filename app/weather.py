import requests

def get_coordinates(city):
    opencage_api_key = 'b9ba98c2aaa249b8b4c972117ec90252'  
    api_url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={opencage_api_key}"
    response = requests.get(api_url)
    data = response.json()
    if data['results']:
        coordinates = data['results'][0]['geometry']
        return coordinates['lat'], coordinates['lng']
    else:
        raise Exception("ОШИБКА: Невозможно найти координаты для города.")

def get_weather(city):
    try:
        lat, lon = get_coordinates(city)
        weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
        weather_response = requests.get(weather_api_url)
        weather_data = weather_response.json()
        weather_info = {
            'city': city,
            'temperature': weather_data['hourly']['temperature_2m'][0]
        }
        return weather_info
    except Exception as e:
        return str(e)

def get_city_suggestions(query):
    geonames_api_key = 'impro'  
    api_url = f"http://api.geonames.org/searchJSON?q={query}&maxRows=5&username={geonames_api_key}"
    response = requests.get(api_url)
    return response.json()
