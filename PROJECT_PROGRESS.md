# Crop Recommendation System Progress

## Phase 1 ✅ Completed

- Installed Docker Desktop
- Configured WSL2
- Started Hadoop Cluster
- Verified HDFS
- Uploaded Crop_recommendation.csv to HDFS
- Created GitHub Repository
- Organized Project Structure

## Current Status

- Hadoop ✅
- HDFS ✅
- Hive ⏳
- Spark ⏳
- ML ⏳
- Streamlit ⏳

upadation from 07-09-2026
# Crop Recommendation System - Project Progress

## Project Overview
A Big Data-based Crop Recommendation System that integrates Hadoop, Hive, Spark, Flask, and Machine Learning to provide crop recommendations using environmental data.

---

## Completed Milestones

### ✅ Milestone 1 - Project Setup
**Status:** Completed

#### Completed
- Created GitHub repository
- Organized project directory structure
- Configured `.gitignore`
- Created Python virtual environment
- Installed Flask and project dependencies
- Generated `requirements.txt`

---

### ✅ Milestone 2 - Big Data Infrastructure
**Status:** Completed

#### Completed
- Configured Docker Compose cluster
- Built custom Hadoop, Hive, and Spark Docker images
- Fixed Windows CRLF entrypoint issue
- Resolved Docker port conflicts
- Configured container networking
- Started Hadoop NameNode and ResourceManager
- Started two Hadoop DataNodes
- Initialized Hive Metastore with PostgreSQL
- Started Spark Master successfully

#### Issues Solved
- Missing Docker entrypoint script
- Windows line-ending (CRLF) compatibility
- Port 9870 already in use
- Hostname resolution (`master`)
- Hive metastore schema initialization

---

### ✅ Milestone 3 - Flask Backend
**Status:** Completed

#### Completed
- Created Flask backend
- Modular project structure
- Blueprint-based routing
- Service layer architecture
- Root endpoint (`/`)
- Health endpoint (`/api/health`)
- Version endpoint (`/api/version`)

#### Backend Structure

backend/
├── app.py
├── config.py
├── routes/
├── services/
├── templates/
└── static/

---

### ✅ Milestone 4 - Live Weather Integration
**Status:** Completed

#### Completed
- Installed Geopy
- Implemented Weather Service
- Integrated Open-Meteo API
- Converted city names to coordinates
- Retrieved live:
  - Temperature
  - Humidity
  - Rainfall
- Added Weather API endpoint

#### Working Endpoint

GET /api/weather/<location>

Example:

GET /api/weather/Thrissur

Response:

{
    "location": "Thrissur",
    "latitude": 10.5270099,
    "longitude": 76.214621,
    "temperature": 29.8,
    "humidity": 71,
    "rainfall": 0.2
}

---

---

### ✅ Milestone 5 - Environment Service
**Status:** Completed

#### Completed
- Refactored backend service architecture
- Standardized service naming convention
- Created `environment_service.py`
- Created `soil_service.py` with placeholder soil values
- Refactored `weather_service.py` to work with latitude and longitude
- Implemented a unified Environment Service
- Added `/api/environment` endpoint
- Successfully combined weather and soil data into a single JSON response
- Validated latitude and longitude query parameters
- Tested the endpoint successfully

#### API Endpoint

GET /api/environment?lat=<latitude>&lon=<longitude>

Example:

GET /api/environment?lat=10.5270&lon=76.2146

Response:

```json
{
    "location": {
        "latitude": 10.5270,
        "longitude": 76.2146
    },
    "weather": {
        "temperature": 29.8,
        "humidity": 71,
        "rainfall": 0.2
    },
    "soil": {
        "nitrogen": 42,
        "phosphorus": 18,
        "potassium": 31,
        "ph": 6.6
    }
}
```

#### Challenges Solved
- Fixed `ModuleNotFoundError` caused by an incorrectly named file (`enviornment_services.py`)
- Improved backend architecture by separating responsibilities into dedicated service modules
- Established a clean service layer for future Hive, Spark, and ML integration

---

## Current Tech Stack

### Backend
- Python
- Flask

### Big Data
- Hadoop
- HDFS
- Hive
- Spark

### Database
- PostgreSQL (Hive Metastore)

### APIs
- Open-Meteo
- Geopy (Nominatim)

### Version Control
- Git
- GitHub

---

## Current Status

Backend: ✅ Working

Docker Cluster: ✅ Running

Hadoop: ✅ Running

Hive: ✅ Running

Spark Master: ✅ Running

Weather API: ✅ Working

Environment API: ✅ Working

Environment Service: ✅ Completed

Soil Service (Placeholder): ✅ Completed

Hive Data Integration: 🔄 Next Milestone

Machine Learning Integration: ⏳ Pending

Frontend Integration: ⏳ Pending