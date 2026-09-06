from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return {
        "message": "Crop Recommendation Backend is Running 🚀",
        "status": "success"
    }


if __name__ == "__main__":
    app.run(debug=True)