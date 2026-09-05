# Crop Recommendation System Docker Infrastructure

This Compose stack runs a single-node Hadoop 3.2.1 cluster with HDFS and YARN, Hive 3.1.3 with a PostgreSQL metastore and HiveServer2, and Spark 3.1.2 master/worker services. All JVM data services share the same Hadoop client configuration and communicate through the internal Docker network.

## Prerequisites

- Docker Desktop with Compose v2 enabled.
- At least 6 GB of Docker memory and 4 CPU cores allocated.
- Ports `5432`, `8020`, `7077`, `8080`, `8081`, `8088`, `9870`, `9864`, `9083`, `10000`, and `10002` available on the host.

## Start the stack

1. Open a terminal in this directory.
2. Create your local environment file: `Copy-Item .env.example .env` in PowerShell, or `cp .env.example .env` in a POSIX shell.
3. Set strong, identical values for `POSTGRES_PASSWORD` and `HIVE_METASTORE_DB_PASSWORD` in `.env`. The Hive metastore authenticates to the PostgreSQL role created from `POSTGRES_USER`.
4. Build and start: `docker compose up -d --build`.
5. Follow first-start initialization: `docker compose logs -f namenode hive-metastore hiveserver2`.

The NameNode and DataNode data plus PostgreSQL data are persisted in named Docker volumes. `docker compose down` preserves them; `docker compose down -v` deliberately deletes the entire local cluster state.

## Service endpoints

| Service | Address |
| --- | --- |
| HDFS NameNode | http://localhost:9870 |
| YARN ResourceManager | http://localhost:8088 |
| Spark Master | http://localhost:8080 |
| Spark Worker | http://localhost:8081 |
| HiveServer2 JDBC | `jdbc:hive2://localhost:10000/default` |
| HiveServer2 web UI | http://localhost:10002 |
| Hive Metastore | `thrift://localhost:9083` |

## HDFS workflow compatibility

The `hdfs-bootstrap` service creates these paths during the first successful start:

```text
/user/hadoop
/user/hive/warehouse
/crop_recommendation_system/input
/crop_recommendation_system/output
```

Use `hdfs://namenode:8020` from services in this Compose network. From a host process, use WebHDFS through port `9870`, or run the HDFS client in the NameNode container. For an existing workflow, upload source data into the existing project path:

```powershell
docker compose cp ..\data\crop_data.csv namenode:/tmp/crop_data.csv
docker compose exec namenode hdfs dfs -put -f /tmp/crop_data.csv /crop_recommendation_system/input/
docker compose exec namenode hdfs dfs -ls /crop_recommendation_system/input
```

If your workflow uses another HDFS directory, create it with `docker compose exec namenode hdfs dfs -mkdir -p /your/path`; the existing data is never removed by the bootstrap script.

## Verification

Run the following after `docker compose ps` reports the long-running services as healthy or running:

```powershell
# HDFS reports one live DataNode and the expected project directories.
docker compose exec namenode hdfs dfsadmin -report
docker compose exec namenode hdfs dfs -ls /crop_recommendation_system

# YARN has a registered NodeManager.
docker compose exec resourcemanager yarn node -list

# HiveServer2 can query the PostgreSQL-backed metastore.
docker compose exec hiveserver2 beeline -u 'jdbc:hive2://localhost:10000/default' -e 'SHOW DATABASES;'

# Spark can read the same HDFS namespace.
docker compose exec spark-master spark-submit --master spark://spark-master:7077 --conf spark.hadoop.fs.defaultFS=hdfs://namenode:8020 --class org.apache.spark.examples.SparkPi $SPARK_HOME/examples/jars/spark-examples_2.12-3.1.2.jar 10
```

Successful output includes a live DataNode, a NodeManager entry, the `default` Hive database, and a Spark `Pi is roughly` result.

## Operational notes

- This is a single-node development/deployment stack, so HDFS replication is `1`.
- The stack intentionally has no Kerberos, TLS, or external secret manager. Put it behind a trusted network boundary and replace the local `.env` secrets before any shared deployment.
- To inspect failures, use `docker compose logs --tail=200 <service>`. To restart one service after a configuration change, use `docker compose up -d --build <service>`.
