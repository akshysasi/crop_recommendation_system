import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, desc

# Get the absolute path to the backend folder
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.environ.get("PREDICTION_DATA_PATH", os.path.join(BASE_DIR, "data", "prediction_history.csv"))


def get_prediction_statistics():

    # Create Spark Session
    builder = (
        SparkSession.builder
        .appName("CropAnalytics")
        .master(os.environ.get("SPARK_MASTER_URL", "local[*]"))
    )
    if os.environ.get("SPARK_ENABLE_HIVE", "").lower() == "true":
        builder = builder.enableHiveSupport()
    driver_host = os.environ.get("SPARK_DRIVER_HOST")
    if driver_host:
        builder = builder.config("spark.driver.host", driver_host).config(
            "spark.driver.bindAddress", "0.0.0.0"
        )
    spark = builder.getOrCreate()

    # Read prediction history
    df = (
        spark.read
        .option("header", True)
        .csv(DATA_PATH, inferSchema=True)
    )

    # Total predictions
    total_predictions = df.count()

    # Most recommended crop
    most_recommended = (
        df.groupBy("predicted_crop")
        .count()
        .orderBy(desc("count"))
        .first()
    )

    # Average temperature
    avg_temp = df.select(avg("temperature")).first()[0]

    # Average rainfall
    avg_rainfall = df.select(avg("rainfall")).first()[0]

    # Crop distribution
    crop_distribution_df = (
        df.groupBy("predicted_crop")
        .count()
        .orderBy(desc("count"))
    )

    crop_distribution = {
        row["predicted_crop"]: row["count"]
        for row in crop_distribution_df.collect()
    }

    spark.stop()

    return {
        "total_predictions": total_predictions,
        "most_recommended_crop": most_recommended["predicted_crop"],
        "recommendation_count": most_recommended["count"],
        "average_temperature": round(avg_temp, 2),
        "average_rainfall": round(avg_rainfall, 2),
        "crop_distribution": crop_distribution
    }