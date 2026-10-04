from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Crop Recommendation Analysis") \
    .master("spark://spark-master:7077") \
    .enableHiveSupport() \
    .getOrCreate()

print("Spark session started successfully!")

# Read the cleaned crop data from Hive
df = spark.table("default.crop_data_clean")

print("Total records:", df.count())

print("Schema:")
df.printSchema()

print("First 10 records:")
df.show(10)

spark.stop()