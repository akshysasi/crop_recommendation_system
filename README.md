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

🌱 Crop Recommendation System — Progress Log
Project: Crop Recommendation System
Working directory: D:\bigdataproject\crop_recommendation_system
1. Project objective
The project combines an existing crop-recommendation ML model with a Big Data processing pipeline.
The Big Data component processes agricultural data containing:
- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- pH
- Rainfall
- Crop label
The goal of the current Big Data layer is to store, clean, process, and analyze this data using Hadoop, Hive, and Spark.
2. Current architecture
                 Crop_recommendation.csv
                          │
                          ▼
                     ┌─────────┐
                     │  HDFS   │
                     └────┬────┘
                          │
                          ▼
                    ┌───────────┐
                    │   Hive    │
                    │ crop_data │
                    └─────┬─────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Hive Cleaning   │
                 │ crop_data_clean │
                 └───────┬─────────┘
                         │
                         ▼
                    ┌─────────┐
                    │ PySpark │
                    └────┬────┘
                         │
                         ▼
              Crop-wise aggregation
                         │
                         ▼
                     ┌───────┐
                     │ HDFS  │
                     └───┬───┘
                         │
                         ▼
              ┌──────────────────┐
              │ Hive EXTERNAL    │
              │ crop_statistics  │
              └──────────────────┘

3. Docker infrastructure
Our project-specific Docker stack contains:
NameNode
DataNode
HDFS Bootstrap
ResourceManager
NodeManager
PostgreSQL
Hive Metastore
HiveServer2
Spark Master
Spark Worker

The stack is running on its own Docker network:
crop-recommendation_default

We deliberately kept the older unrelated Hadoop/Hive/Spark Docker stack untouched.
4. HDFS setup ✅
HDFS is working correctly.
The project has:
/crop_recommendation_system/
├── input/
└── output/

The original dataset was uploaded to:
/crop_recommendation_system/input/Crop_recommendation.csv

Dataset size in HDFS:
149263 bytes

HDFS health was verified:
Live DataNodes: 1
Under replicated blocks: 0
Corrupt replicas: 0
Missing blocks: 0

So the HDFS layer is healthy.
5. Hive raw table ✅
Created:
crop_data

Columns:
Nitrogen       INT
phosphorus     INT
potassium      INT
temperature    DOUBLE
humidity       DOUBLE
ph             DOUBLE
rainfall       DOUBLE
label          STRING

The raw CSV contains its header as a row, so the raw table contains:
2201 rows

including the header.
6. Hive cleaned table ✅
Created:
crop_data_clean

The cleaning process:
- removes the CSV header row
- converts numeric fields to the appropriate types
- produces the clean dataset
Final count:
2200 records

Schema:
nitrogen       INT
phosphorus     INT
potassium      INT
temperature    DOUBLE
humidity       DOUBLE
ph             DOUBLE
rainfall       DOUBLE
label          STRING

7. Spark + Hive integration ✅
Spark initially couldn't see the Hive tables.
We fixed this by adding:
docker/config/spark/hive-site.xml

with the Hive Metastore connection:
thrift://hive-metastore:9083

After recreating the Spark containers, Spark successfully detected:
crop_data
crop_data_clean

8. Spark Python environment ✅
The Spark image initially didn't contain Python 3.
This caused:
Cannot run program "python3"

We updated the Spark Dockerfile to install Python 3.
Current Spark containers successfully run:
Python 3.10.12

9. Spark cluster verification ✅
Spark Master and Worker are working.
SparkPi was successfully executed:
Pi is roughly 3.142...

This confirmed that the Spark cluster itself was functional.
10. PySpark analytics ✅
Our main Spark script:
spark/crop_analysis.py

reads:
df = spark.table("default.crop_data_clean")


Then performs:
df.groupBy("label").agg(...)


and calculates average:
Nitrogen
Phosphorus
Potassium
Temperature
Humidity
pH
Rainfall

for each crop.
11. Crop-wise statistics ✅
Spark successfully processed all:
2200 records

and generated statistics for:
22 crops

Examples:
rice
79.89 N
47.58 P
39.87 K
23.69°C
82.27 humidity
6.43 pH
236.18 rainfall

and:
apple
20.80 N
134.22 P
199.89 K
22.63°C
92.33 humidity
5.93 pH
112.65 rainfall

This confirms that we're doing actual distributed data processing with Spark, rather than simply loading the CSV in Python.
12. Spark → HDFS persistence ✅
The processed statistics are written to:
/crop_recommendation_system/output/crop_statistics

We initially got multiple Spark partition files.
We improved this using:
crop_stats = crop_stats.coalesce(1)


Because we're only writing 22 aggregated records, a single output partition is appropriate here.
Final HDFS structure:
crop_statistics/
├── _SUCCESS
└── part-00000-....csv

The CSV contains:
22 crop records

with the header:
label,avg_nitrogen,avg_phosphorus,avg_potassium,
avg_temperature,avg_humidity,avg_ph,avg_rainfall

13. Hive processed statistics table ✅
We created:
crop_statistics

The important correction we made here was changing it to:
EXTERNAL_TABLE

rather than a managed Hive table.
It points to:
hdfs://namenode:8020/crop_recommendation_system/output/crop_statistics

and skips the CSV header:
skip.header.line.count = 1

Hive successfully queries the processed data.
Example:
chickpea | 40.09 | 67.79 | 79.92 | ...
mungbean | 20.99 | 47.28 | 19.87 | ...
orange   | 19.58 | 16.55 | 10.01 | ...

14. Important lesson learned ⚠️
We accidentally created crop_statistics as a managed Hive table initially.
When we dropped it, Hive removed the files from its managed location.
Fortunately:
- the original dataset remained safe
- HDFS remained healthy
- the processed output was regenerated through Spark
- the table was converted to an external table
New project rule:
Always check whether a Hive table is MANAGED or EXTERNAL before dropping it.
For data that already exists in HDFS and should survive Hive metadata changes, use:
CREATE EXTERNAL TABLE

This is now our correct approach.
15. Git progress ✅
Current Git history:
b30555e  Save crop statistics to HDFS
92af9b3  Add crop-wise Spark analytics
62648c6  Connect Spark to Hive and add crop analysis
15cfb14  Add Python to Spark image
68ed22f  Add initial Spark analysis job

Current state:
main → origin/main
working tree clean

We also created the SQL documentation directory:
sql/
├── create_raw_table.sql
├── create_clean_table.sql
└── create_statistics_table.sql

These document the Hive setup so the pipeline can be reproduced instead of relying on commands buried in terminal history.
🚀 Current milestone
We're currently here:
                    BIG DATA PIPELINE
                           │
                           ▼
                     HDFS + Hive
                           │
                           ▼
                       PySpark
                           │
                           ▼
                  Processed analytics
                           │
                           ▼
                    HDFS + Hive
                           │
                           ▼
                    ✅ COMPLETE

Next major phase
Integrate this Big Data layer with the existing Flask application.
That means we'll eventually have:
User selects location
        ↓
Flask
        ↓
Location → coordinates
        ↓
Weather data
        ↓
Soil/environment inputs
        ↓
Existing ML model
        ↓
Crop recommendation

while our Big Data infrastructure provides the large-scale agricultural data processing/analytics layer behind the project.
And importantly, we are not retraining or replacing your existing ML model. We're building the Big Data component around it.