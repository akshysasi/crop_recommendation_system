# 🌾 AI-Powered Crop Recommendation System
## Project Progress Tracker

**Last Updated:** 14 September 2026

---

# Overall Progress

**Project Completion:** **~92%**

---

# ✅ Completed

## Phase 1 – Project Setup
- [x] Repository created
- [x] Git initialized
- [x] Virtual environment configured
- [x] Project folder structure created

---

## Phase 2 – Dataset & Machine Learning

### Data Preparation
- [x] Dataset imported
- [x] Removed unnecessary columns
- [x] Renamed dataset columns
- [x] Checked data types
- [x] Checked null values
- [x] Verified duplicate records
- [x] Exploratory Data Analysis (EDA)

### Model Training
- [x] Label Encoding
- [x] Feature Selection
- [x] Train-Test Split
- [x] Compared multiple ML algorithms
- [x] Selected Gaussian Naive Bayes
- [x] Trained final model
- [x] Saved trained model (.pkl)
- [x] Saved Label Encoder (.pkl)

---

## Phase 3 – Backend Development

- [x] Flask application created
- [x] REST API implemented
- [x] Prediction endpoint created
- [x] Model integrated into backend
- [x] CORS configured
- [x] Prediction service completed

---

## Phase 4 – Frontend Development

- [x] HTML interface
- [x] CSS styling
- [x] JavaScript integration
- [x] Connected frontend with Flask API
- [x] End-to-end prediction working

---

## Phase 5 – Prediction History

- [x] Prediction logging implemented
- [x] Automatic CSV creation
- [x] Automatic CSV header generation
- [x] Prediction history stored successfully

---

## Phase 6 – Apache Spark Integration

- [x] PySpark installed
- [x] Java configured
- [x] Spark compatibility issues resolved
- [x] Spark analytics service created
- [x] Analytics API endpoint implemented
- [x] Crop distribution analytics added

### Current Analytics

- [x] Total Predictions
- [x] Most Recommended Crop
- [x] Recommendation Count
- [x] Average Temperature
- [x] Average Rainfall
- [x] Crop Distribution

---

## Phase 7 – Documentation

- [x] README updated
- [x] Git commits maintained throughout development
- [x] Project structure documented

---

# 🚧 In Progress

## Apache Hive Integration

Status: **Paused**

Current findings:

- Docker Desktop installed and working.
- Existing Hadoop/Hive Docker cluster detected.
- Project also contains its own Docker-based Hadoop/Hive setup.
- Docker port conflict on PostgreSQL (5432).
- HiveServer2 in the old stack is not starting correctly.
- Decision made to pause and complete Hive setup in a dedicated session.

---

# ⏳ Remaining Work

## Big Data

- [ ] Finalize Hadoop/Hive Docker environment
- [ ] Start Hive Metastore
- [ ] Start HiveServer2
- [ ] Import `prediction_history.csv`
- [ ] Create Hive database
- [ ] Create Hive table
- [ ] Execute Hive SQL queries
- [ ] (Optional) Integrate Hive queries with Flask

---

## Frontend Improvements

- [ ] Improve UI styling
- [ ] Add loading indicator
- [ ] Improve result display
- [ ] Input validation
- [ ] Optional analytics dashboard

---

## Documentation

- [ ] Final architecture diagram
- [ ] Installation guide
- [ ] Screenshots
- [ ] Demo guide
- [ ] Viva preparation

---

## Deployment

- [ ] Dockerize Flask backend (optional)
- [ ] Final deployment/testing

---

# Git Milestones

- ✅ Project initialization
- ✅ Dataset cleaning
- ✅ Model training
- ✅ Model serialization
- ✅ Flask backend
- ✅ Prediction API
- ✅ Frontend integration
- ✅ Prediction history logging
- ✅ PySpark compatibility fix
- ✅ Apache Spark analytics
- ✅ Crop distribution analytics
- ✅ README update

---

# Next Session Plan

1. Review the existing Docker Hadoop/Hive environments.
2. Remove or isolate conflicting Docker stacks.
3. Bring up the project's Hadoop/Hive Docker stack.
4. Verify Hive Metastore and HiveServer2.
5. Import `prediction_history.csv` into Hive.
6. Run Hive SQL analytics.
7. Complete the Big Data integration.

---

# Current Status

| Component | Status |
|----------|--------|
| Machine Learning | ✅ Complete |
| Flask Backend | ✅ Complete |
| Frontend | ✅ Complete |
| Prediction API | ✅ Complete |
| Prediction Logging | ✅ Complete |
| Apache Spark | ✅ Complete |
| Spark Analytics | ✅ Complete |
| Apache Hive | 🚧 In Progress |
| Documentation |  Complete |
| Deployment | ⏳ Pending |

---

## 🎯 Overall Progress

**≈ 92% Complete**

The application is fully functional with machine learning predictions, historical logging, and Apache Spark analytics. The remaining major task is completing the Apache Hive integration and applying final project polish.

## 2026-10-02 — Big Data Stack Verification & Spark Troubleshooting

- Completed and verified the Dockerized Big Data environment:
  - Hadoop HDFS — NameNode and DataNode
  - YARN — ResourceManager and NodeManager
  - Hive — Hive Metastore and HiveServer2
  - PostgreSQL — Hive metadata database
  - Spark — Master and Worker
- Verified HDFS:
  - 1 live DataNode
  - 0 missing blocks
  - 0 corrupt blocks
  - 0 under-replicated blocks
  - `/crop_recommendation_system/input` and `/crop_recommendation_system/output` directories available.
- Verified YARN with 1 running NodeManager.
- Verified HiveServer2 by successfully executing `SHOW DATABASES`.
- Investigated a SparkPi job that was taking abnormally long. Logs showed the Spark Worker losing its heartbeat, being removed by the Master, and subsequently re-registering.
- Restarted only the project's `spark-master` and `spark-worker` containers.
- Verified the Worker re-registered successfully and returned to an `ALIVE` state.
- Re-ran SparkPi successfully:
  - Exit code: `0`
  - Result: `Pi is roughly 3.1422551422551424`
- No project files were changed during the Spark troubleshooting.
- No Docker volumes or unrelated Docker stacks were touched.
- Git working tree remains clean and up to date.