from flask import Blueprint, request
from services.weather_service import get_weather
from services.environment_service import get_environment
from services.prediction_service import predict_crop

api = Blueprint("api", __name__)


@api.route("/health", methods=["GET"])
def health():
    return {
        "status": "healthy",
        "service": "Crop Recommendation Backend",
        "version": "1.0.0"
    }


@api.route("/version", methods=["GET"])
def version():
    return {
        "backend": "Flask",
        "version": "1.0.0"
    }


# Temporary endpoint for testing weather by city name
@api.route("/weather/<location>", methods=["GET"])
def weather(location):
    return get_weather(location)


# Main endpoint for the project
@api.route("/environment", methods=["GET"])
def environment():

    try:
        latitude = float(request.args.get("lat"))
        longitude = float(request.args.get("lon"))
    except (TypeError, ValueError):
        return {
            "error": "Latitude and longitude must be valid numbers."
        }, 400

    return get_environment(latitude, longitude)
@api.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    required_fields = [
        "nitrogen",
        "phosphorus",
        "potassium",
        "temperature",
        "humidity",
        "ph",
        "rainfall"
    ]

    for field in required_fields:
        if field not in data:
            return {
                "error": f"Missing field: {field}"
            }, 400

    return predict_crop(
        data["nitrogen"],
        data["phosphorus"],
        data["potassium"],
        data["temperature"],
        data["humidity"],
        data["ph"],
        data["rainfall"]
    )