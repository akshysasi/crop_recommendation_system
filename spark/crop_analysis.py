from pyspark.sql import SparkSession
from pyspark.sql.functions import avg

spark = SparkSession.builder \
    .appName("Crop Recommendation Analysis") \
    .master("spark://spark-master:7077") \
    .enableHiveSupport() \
    .getOrCreate()

print("Spark session started successfully!")

# Read cleaned crop data from Hive
df = spark.table("default.crop_data_clean")

print("Total records:", df.count())

# Calculate crop-wise average values
crop_stats = df.groupBy("label").agg(
    avg("nitrogen").alias("avg_nitrogen"),
    avg("phosphorus").alias("avg_phosphorus"),
    avg("potassium").alias("avg_potassium"),
    avg("temperature").alias("avg_temperature"),
    avg("humidity").alias("avg_humidity"),
    avg("ph").alias("avg_ph"),
    avg("rainfall").alias("avg_rainfall")
)

print("Crop-wise average statistics:")
crop_stats.show(22, truncate=False)

crop_stats = crop_stats.coalesce(1)

# Save crop-wise statistics to HDFS
output_path = "hdfs://namenode:8020/crop_recommendation_system/output/crop_statistics"

crop_stats.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(output_path)

print("Crop statistics successfully saved to HDFS!")

spark.stop()