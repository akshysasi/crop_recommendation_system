from flask import Flask
from routes.api import api

app = Flask(__name__)

# Register API routes
app.register_blueprint(api, url_prefix="/api")


@app.route("/")
def home():
    return {
        "message": "Crop Recommendation System Backend",
        "status": "running"
    }


if __name__ == "__main__":
    app.run(debug=True)