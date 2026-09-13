# 🌾 AI-Powered Crop Recommendation System

An AI and Big Data based Crop Recommendation System that predicts the most suitable crop using soil nutrients and environmental parameters. The system also logs prediction history and performs analytics using Apache Spark.

---

## 🚀 Features

- 🌱 Crop recommendation using Machine Learning
- 📊 Trained Gaussian Naive Bayes model
- 🌐 Interactive web interface
- ⚙️ Flask REST API
- 📁 Prediction history logging
- ⚡ Apache Spark analytics
- 📈 Dataset exploration and model comparison

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS

### Machine Learning
- Pandas
- NumPy
- Scikit-learn
- Joblib

### Big Data
- Apache Spark (PySpark)

### Development Tools
- VS Code
- Jupyter Notebook
- Git & GitHub

---

## 📂 Project Structure

```
crop_recommendation_system/
│
├── backend/
│   ├── data/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── app.py
│   └── requirements.txt
│
├── dataset/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── notebooks/
│   └── crop_model_training.ipynb
│
└── README.md
```

---

## 🤖 Machine Learning Pipeline

1. Dataset Loading
2. Data Cleaning
3. Exploratory Data Analysis (EDA)
4. Feature Selection
5. Label Encoding
6. Train-Test Split
7. Model Comparison
8. Model Training
9. Model Export
10. Backend Integration

---

## ⚡ Spark Analytics

Every prediction is stored in:

```
backend/data/prediction_history.csv
```

Spark analyzes this data to generate:

- Total Predictions
- Most Recommended Crop
- Average Temperature
- Average Rainfall

Analytics Endpoint:

```
GET /api/analytics
```

---

## 🌐 API Endpoints

### Predict Crop

```
POST /api/predict
```

Example Request

```json
{
    "nitrogen": 90,
    "phosphorus": 42,
    "potassium": 43,
    "temperature": 20.87,
    "humidity": 82.0,
    "ph": 6.5,
    "rainfall": 202.9
}
```

Example Response

```json
{
    "recommended_crop": "rice"
}
```

---

### Analytics

```
GET /api/analytics
```

Example Response

```json
{
    "total_predictions": 3,
    "most_recommended_crop": "banana",
    "recommendation_count": 1,
    "average_temperature": 24.29,
    "average_rainfall": 150.67
}
```

---

## 📊 Current Project Status

- ✅ Frontend Completed
- ✅ Flask Backend Completed
- ✅ Machine Learning Model Integrated
- ✅ Prediction History Logging
- ✅ Apache Spark Analytics
- ⏳ Apache Hive Integration
- ⏳ Deployment

---

## 👨‍💻 Authors

Developed as an AI & Big Data academic project.
---

## 👨‍💻 Team Members

- Akshay K Sasi
- Al Ameen
- Albin Abraham
- Surag S.

---

