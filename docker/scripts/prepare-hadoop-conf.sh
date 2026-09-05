#!/usr/bin/env bash

prepare_hadoop_conf() {
  : "${HDFS_NAMENODE_DIR:=/data/dfs/name}"
  : "${HDFS_DATANODE_DIR:=/data/dfs/data}"
  : "${HDFS_REPLICATION:=1}"
  export HDFS_NAMENODE_DIR HDFS_DATANODE_DIR HDFS_REPLICATION

  local runtime_conf=/tmp/hadoop-conf
  rm -rf "$runtime_conf"
  mkdir -p "$runtime_conf"
  cp -a /opt/hadoop/etc/hadoop/. "$runtime_conf/"
  sed -i \
    -e "s|\${HDFS_NAMENODE_DIR}|${HDFS_NAMENODE_DIR}|g" \
    -e "s|\${HDFS_DATANODE_DIR}|${HDFS_DATANODE_DIR}|g" \
    -e "s|\${HDFS_REPLICATION}|${HDFS_REPLICATION}|g" \
    "$runtime_conf/hdfs-site.xml"
  export HADOOP_CONF_DIR="$runtime_conf"
}
