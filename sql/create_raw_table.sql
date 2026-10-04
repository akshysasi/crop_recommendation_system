CREATE TABLE IF NOT EXISTS crop_data (
    Nitrogen INT,
    phosphorus INT,
    potassium INT,
    temperature DOUBLE,
    humidity DOUBLE,
    ph DOUBLE,
    rainfall DOUBLE,
    label STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
STORED AS TEXTFILE
LOCATION '/crop_recommendation_system/input';