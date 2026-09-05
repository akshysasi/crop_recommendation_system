#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/prepare-hadoop-conf.sh"
prepare_hadoop_conf

until hdfs dfs -ls / >/dev/null 2>&1; do
  echo "Waiting for HDFS..."
  sleep 2
done

hdfs dfs -mkdir -p /tmp /user/hadoop /user/hive/warehouse
hdfs dfs -mkdir -p /crop_recommendation_system/input /crop_recommendation_system/output
hdfs dfs -chmod 1777 /tmp
hdfs dfs -chmod -R 775 /user/hive /crop_recommendation_system

echo "HDFS bootstrap completed."
