import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, desc

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.environ.get(
    "PREDICTION_DATA_PATH",
    os.path.join(BASE_DIR, "data", "prediction_history.csv"),
)


def _spark_session():
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
    return builder.getOrCreate()


def get_prediction_statistics():
    spark = _spark_session()

    # Keep the existing prediction-history analytics response intact.
    df = (
        spark.read
        .option("header", True)
        .csv(f"file://{DATA_PATH}", inferSchema=True)
    )
    total_predictions = df.count()
    most_recommended = (
        df.groupBy("predicted_crop")
        .count()
        .orderBy(desc("count"))
        .first()
    )
    avg_temp = df.select(avg("temperature")).first()[0]
    avg_rainfall = df.select(avg("rainfall")).first()[0]
    crop_distribution = {
        row["predicted_crop"]: row["count"]
        for row in (
            df.groupBy("predicted_crop")
            .count()
            .orderBy(desc("count"))
            .collect()
        )
    }

    result = {
        "total_predictions": total_predictions,
        "most_recommended_crop": most_recommended["predicted_crop"],
        "recommendation_count": most_recommended["count"],
        "average_temperature": round(avg_temp, 2),
        "average_rainfall": round(avg_rainfall, 2),
        "crop_distribution": crop_distribution,
    }

    if os.environ.get("SPARK_ENABLE_HIVE", "").lower() == "true":
        statistics = spark.table("default.crop_statistics").orderBy("label")
        result["crop_statistics"] = [row.asDict() for row in statistics.collect()]

    return result
