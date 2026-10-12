# Crop Recommendation System

An agricultural crop recommendation application that combines a trained Gaussian Naive Bayes model and a Flask API with a browser dashboard and a Hadoop, Hive, and Spark data pipeline. The model is already checked in; the documented workflow does not retrain it.

## Features and architecture

- The browser UI in `frontend/` sends requests to the Flask API on port 5000. The frontend is a separate static site; serve its directory with VS Code Live Server or another static HTTP server (the project progress log records Live Server at `http://localhost:5500/`).
- Flask serves prediction, history analytics, health, version, weather, and environment routes. Predictions are appended to `backend/data/prediction_history.csv`.
- The analytics service uses PySpark and the Compose Spark master. The API's prediction analytics and the batch agricultural dataset pipeline are separate flows.
- The Compose stack in `docker/` defines Hadoop HDFS and YARN, PostgreSQL-backed Hive Metastore and HiveServer2, Spark master and worker, and the Flask backend. Its network is `crop-recommendation-default`; its named volumes persist HDFS and PostgreSQL data.
- The batch pipeline loads `dataset/Crop_recommendation.csv` into HDFS, uses Hive raw and cleaned tables, aggregates crop statistics with `spark/crop_analysis.py`, writes results to HDFS, and exposes them through the Hive external `crop_statistics` table. Reproduction SQL is in `sql/`.
- Environment lookup uses Open-Meteo for weather and currently returns fixed placeholder soil values from `backend/services/soil_service.py`.

## Prerequisites

- Docker Desktop running Linux containers, with Docker Compose v2.
- At least 6 GB memory and 4 CPU cores allocated to Docker, as stated in `docker/README.md`.
- Host ports used by the stack must be available: 15432, 18020, 17077, 18082, 18081, 18088, 19870, 19864, 19083, 11000, 11002, 18042, and 5000. The optional frontend server uses 5500.
- A browser and VS Code Live Server (or another static server) to view the frontend.
- `docker/.env` with `POSTGRES_PASSWORD` and `HIVE_METASTORE_DB_PASSWORD`. `docker/.env.example` is the template; keep secrets local.
- For running the Flask application outside Docker, use a Python environment and install the dependencies in `requirements.txt`; Spark analytics additionally needs a compatible Java/Spark setup. The checked-in Docker image supplies Java and Spark.

## Start and stop

From the repository root, in PowerShell:

```powershell
Set-Location .\docker
Copy-Item .env.example .env # only on first setup; set both password values in .env
docker compose up -d --build
docker compose ps
```

Open `..\frontend\index.html` with VS Code Live Server, or serve the `../frontend/` directory using another static server. The project has previously used `http://localhost:5500/`; this URL depends on the chosen static server. The dashboard calls `http://localhost:5000/api`.

To stop the Compose services while preserving their volumes, run `docker compose stop` or `docker compose down` from `docker/`. **Do not use `docker compose down -v`** unless intentionally discarding the project's persistent HDFS and PostgreSQL state. Do not use `docker compose down` from the unrelated `hadoop-hive-spark-docker/` stack for this project.

## API

Base URL: `http://localhost:5000/api`

| Method and path | Purpose |
| --- | --- |
| `GET /health` | Backend health response (`status`, service, version). |
| `GET /version` | Backend name and version. |
| `GET /analytics` | Spark-backed prediction-history summary and crop distribution. May take noticeable time. |
| `POST /predict` | Predict from JSON fields `nitrogen`, `phosphorus`, `potassium`, `temperature`, `humidity`, `ph`, and `rainfall`; records the prediction in history. |
| `GET /environment?lat=<latitude>&lon=<longitude>` | Weather plus soil values. Weather requires external Open-Meteo access; soil values are placeholders. |
| `GET /weather/<location>` | Legacy temporary route. Its current handler passes the path string to a latitude/longitude weather function; treat it as nonfunctional pending a code fix. |

Example prediction body (this request changes prediction history):

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

## Data pipeline

1. The source CSV is `dataset/Crop_recommendation.csv`.
2. HDFS input path: `/crop_recommendation_system/input/Crop_recommendation.csv`.
3. Hive SQL scripts in `sql/` define the raw, cleaned, and statistics tables. The progress record reports 2,200 cleaned rows across 22 crops (recorded earlier; not re-queried in this session).
4. `spark/crop_analysis.py` groups cleaned records by crop and calculates average nutrient and environmental values.
5. The statistics output is stored at `/crop_recommendation_system/output/crop_statistics` and registered as an external Hive table, according to the project progress record.
6. Separately, Flask prediction history is written to `backend/data/prediction_history.csv` and used by `/api/analytics`.

## Final system check

Run read-only checks from PowerShell in `docker/` after the stack is already running. These commands do not start, stop, or recreate services:

```powershell
docker compose ps
Invoke-RestMethod http://localhost:5000/api/health
Invoke-RestMethod http://localhost:5000/api/version
Invoke-RestMethod http://localhost:5000/api/analytics # Spark-backed; allow time for completion
Invoke-WebRequest http://localhost:5500/ -UseBasicParsing
Invoke-WebRequest http://localhost:5500/script.js -UseBasicParsing
Invoke-WebRequest http://localhost:5500/style.css -UseBasicParsing
```

If environment access is required and Open-Meteo connectivity is available, check a known coordinate with `Invoke-RestMethod 'http://localhost:5000/api/environment?lat=10.0&lon=76.3'`. This may call the external weather service. An invalid-coordinate validation check that avoids the external call is `Invoke-WebRequest 'http://localhost:5000/api/environment?lat=bad&lon=76.3' -SkipHttpErrorCheck` (expected HTTP 400).

Do not use `POST /api/predict` as a read-only smoke test: it adds a row to prediction history and changes analytics. For a full end-to-end prediction check, choose a test input knowingly and record the resulting history change.

The last system-check attempt in this workspace was **12 October 2026**. Docker Desktop's API pipe denied access, no listeners were found on ports 5000, 5500, 19870, 18088, or 18082, and HTTP requests to the backend and frontend could not be verified. This is an environment limitation, not a passing system test. Earlier progress entries record successful stack, Hive, Spark, analytics, and frontend checks on earlier dates; those results have not been revalidated today.

## Project structure

```text
backend/       Flask app, API routes, model files, services, prediction history
dataset/       Crop recommendation source dataset
docker/        Compose file, Dockerfiles, configs, scripts, and Docker guide
frontend/      Static dashboard HTML, CSS, and JavaScript
notebooks/     Model exploration/training notebooks
report/        Project report materials
screenshots/   Captured project screenshots
soil_retriever/ Soil lookup related project files
spark/         Batch crop analytics job
sql/           Hive table setup scripts
model/         Additional model-related project files
```

## Further infrastructure verification

The more extensive Hadoop/Hive/Spark checks and service addresses are documented in [`docker/README.md`](docker/README.md). Run them only after confirming that the Compose stack is already running. Never format HDFS or remove volumes as part of routine verification.
