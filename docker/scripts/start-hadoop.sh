#!/usr/bin/env bash
set -euo pipefail

role="${1:?Hadoop role is required}"
source "$(dirname "$0")/prepare-hadoop-conf.sh"
prepare_hadoop_conf

case "$role" in
  namenode)
    if [[ ! -f "${HDFS_NAMENODE_DIR}/current/VERSION" ]]; then
      hdfs namenode -format -nonInteractive -clusterId "${CLUSTER_NAME:-crop-recommendation}"
    fi
    exec hdfs namenode
    ;;
  datanode)
    exec hdfs datanode
    ;;
  resourcemanager)
    exec yarn resourcemanager
    ;;
  nodemanager)
    exec yarn nodemanager
    ;;
  *)
    echo "Unsupported Hadoop role: $role" >&2
    exit 64
    ;;
esac
