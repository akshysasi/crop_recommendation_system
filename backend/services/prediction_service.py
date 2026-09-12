import os
import joblib
import pandas as pd

# Get the absolute path to the models folder
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "crop_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

# Load the trained model and label encoder only once
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)


def predict_crop(nitrogen, phosphorus, potassium,
                 temperature, humidity, ph, rainfall):

    # Create input DataFrame with the same feature names used during training
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

    return {
        "recommended_crop": crop
    }