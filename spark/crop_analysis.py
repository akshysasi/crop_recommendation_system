from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Crop Recommendation Analysis") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

print("Spark session started successfully!")