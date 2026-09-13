import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "prediction_history.csv")


def get_prediction_statistics():

    spark = (
        SparkSession.builder
        .appName("CropAnalytics")
        .master("local[*]")
        .getOrCreate()
    )

    df = (
        spark.read
        .option("header", True)
        .csv(DATA_PATH, inferSchema=True)
    )

    total_predictions = df.count()

    most_recommended = (
        df.groupBy("predicted_crop")
        .count()
        .orderBy("count", ascending=False)
        .first()
    )

    avg_temp = df.select(avg("temperature")).first()[0]
    avg_rainfall = df.select(avg("rainfall")).first()[0]

    spark.stop()

    return {
        "total_predictions": total_predictions,
        "most_recommended_crop": most_recommended["predicted_crop"],
        "recommendation_count": most_recommended["count"],
        "average_temperature": round(avg_temp, 2),
        "average_rainfall": round(avg_rainfall, 2)
    }