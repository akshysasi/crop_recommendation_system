import os
import csv
from datetime import datetime

import joblib
import pandas as pd

# Get the absolute path to the backend folder
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "crop_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "prediction_history.csv")

# Load model and label encoder once
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)


def predict_crop(nitrogen, phosphorus, potassium,
                 temperature, humidity, ph, rainfall):

    # Create input DataFrame
    input_data = pd.DataFrame([{
        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }])

    # Predict
    prediction = model.predict(input_data)

    # Convert numeric prediction back to crop name
    crop = label_encoder.inverse_transform(prediction)[0]

    # Save prediction to CSV
    with open(DATA_PATH, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            nitrogen,
            phosphorus,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall,
            crop
        ])

    return {
        "recommended_crop": crop
    }