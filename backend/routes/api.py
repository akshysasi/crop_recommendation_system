from flask import Blueprint
from services.weather_service import get_weather

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
@api.route("/weather/<location>", methods=["GET"])
def weather(location):
    return get_weather(location)