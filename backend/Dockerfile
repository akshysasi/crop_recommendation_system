FROM crop-recommendation-spark:3.1.2 AS spark-runtime

FROM python:3.13-slim
COPY --from=spark-runtime /opt/java/openjdk /opt/java/openjdk
COPY --from=spark-runtime /opt/spark-3.1.2-bin-hadoop3.2 /opt/spark

ENV JAVA_HOME=/opt/java/openjdk \
    SPARK_HOME=/opt/spark \
    PYTHONPATH=/opt/spark/python/pyspark.zip:/opt/spark/python/lib/py4j-0.10.9-src.zip \
    PATH=/opt/java/openjdk/bin:/opt/spark/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir \
      -r requirements.txt \
      Flask-Cors==6.0.5 \
      joblib==1.6.0 \
      scikit-learn==1.9.0

COPY app.py config.py ./
COPY routes/ ./routes/
COPY services/ ./services/
COPY models/ ./models/
COPY templates/ ./templates/
COPY static/ ./static/

EXPOSE 5000
ENV PYTHONPATH=/opt/spark/python/lib/pyspark.zip:/opt/spark/python/lib/py4j-0.10.9-src.zip
CMD ["python", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5000"]
