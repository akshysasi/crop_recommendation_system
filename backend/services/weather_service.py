from geopy.geocoders import Nominatim
import requests


def get_weather(location):
    """
    Fetch current weather data for a given location.
    Returns temperature, humidity and rainfall.
    """

    # Convert location name to latitude and longitude
    geolocator = Nominatim(user_agent="crop_recommendation_system")
    place = geolocator.geocode(location)

    if place is None:
        return {"error": "Location not found"}

    latitude = place.latitude
    longitude = place.longitude

    # Open-Meteo API
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m"
        "&daily=rain_sum"
        "&timezone=auto"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Unable to fetch weather"}

    data = response.json()

    return {
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "temperature": data["current"]["temperature_2m"],
        "humidity": data["current"]["relative_humidity_2m"],
        "rainfall": data["daily"]["rain_sum"][0]
    }