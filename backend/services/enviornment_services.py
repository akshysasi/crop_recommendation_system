from services.weather_service import get_weather
from services.soil_service import get_soil_data


def get_environment(latitude, longitude):
    weather = get_weather(latitude, longitude)
    soil = get_soil_data(latitude, longitude)

    if "error" in weather:
        return weather

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "weather": weather,
        "soil": soil
    }