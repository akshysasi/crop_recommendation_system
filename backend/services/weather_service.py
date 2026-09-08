from requests import get


def get_weather(latitude, longitude):
    """
    Fetch weather using latitude and longitude.
    """

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m"
        "&daily=rain_sum"
        "&timezone=auto"
    )

    response = get(url)

    if response.status_code != 200:
        return {"error": "Unable to fetch weather"}

    data = response.json()

    return {
        "temperature": data["current"]["temperature_2m"],
        "humidity": data["current"]["relative_humidity_2m"],
        "rainfall": data["daily"]["rain_sum"][0]
    }