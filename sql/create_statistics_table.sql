CREATE EXTERNAL TABLE IF NOT EXISTS crop_statistics (
    label STRING,
    avg_nitrogen DOUBLE,
    avg_phosphorus DOUBLE,
    avg_potassium DOUBLE,
    avg_temperature DOUBLE,
    avg_humidity DOUBLE,
    avg_ph DOUBLE,
    avg_rainfall DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/crop_recommendation_system/output/crop_statistics'
TBLPROPERTIES ('skip.header.line.count'='1');