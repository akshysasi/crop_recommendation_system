DROP TABLE IF EXISTS crop_data_clean;

CREATE TABLE crop_data_clean AS
SELECT
    CAST(Nitrogen AS INT) AS nitrogen,
    CAST(phosphorus AS INT) AS phosphorus,
    CAST(potassium AS INT) AS potassium,
    CAST(temperature AS DOUBLE) AS temperature,
    CAST(humidity AS DOUBLE) AS humidity,
    CAST(ph AS DOUBLE) AS ph,
    CAST(rainfall AS DOUBLE) AS rainfall,
    label
FROM crop_data
WHERE label <> 'label';