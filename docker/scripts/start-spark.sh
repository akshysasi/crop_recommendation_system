#!/usr/bin/env bash
set -euo pipefail

role="${1:?Spark role is required}"
source "$(dirname "$0")/prepare-hadoop-conf.sh"
prepare_hadoop_conf
export SPARK_DIST_CLASSPATH="$(hadoop classpath)"

case "$role" in
  master)
    exec "$SPARK_HOME/bin/spark-class" org.apache.spark.deploy.master.Master \
      --host spark-master --port 7077 --webui-port 8080
    ;;
  worker)
    exec "$SPARK_HOME/bin/spark-class" org.apache.spark.deploy.worker.Worker \
      --cores "${SPARK_WORKER_CORES:-2}" --memory "${SPARK_WORKER_MEMORY:-2g}" \
      --webui-port 8081 "spark://spark-master:7077"
    ;;
  *)
    echo "Unsupported Spark role: $role" >&2
    exit 64
    ;;
esac
