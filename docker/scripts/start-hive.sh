#!/usr/bin/env bash
set -euo pipefail

role="${1:?Hive role is required}"
source "$(dirname "$0")/prepare-hadoop-conf.sh"
prepare_hadoop_conf
runtime_conf=/tmp/hive-conf
rm -rf "$runtime_conf"
mkdir -p "$runtime_conf"
cp -a /opt/hive/conf/. "$runtime_conf/"
escape_for_sed() { printf '%s' "$1" | sed 's/[&|\\]/\\&/g'; }
db_password="$(escape_for_sed "$HIVE_METASTORE_DB_PASSWORD")"
db_name="$(escape_for_sed "$HIVE_METASTORE_DB_NAME")"
db_user="$(escape_for_sed "$HIVE_METASTORE_DB_USER")"
sed -i "s|__HIVE_METASTORE_DB_PASSWORD__|${db_password}|g; s|__HIVE_METASTORE_DB_NAME__|${db_name}|g; s|__HIVE_METASTORE_DB_USER__|${db_user}|g" "$runtime_conf/hive-site.xml"
export HIVE_CONF_DIR="$runtime_conf"

case "$role" in
  metastore)
    if ! schematool -dbType postgres -info >/dev/null 2>&1; then
      schematool -dbType postgres -initSchema
    fi
    exec hive --service metastore
    ;;
  hiveserver2)
    until nc -z hive-metastore 9083; do
      echo "Waiting for Hive Metastore..."
      sleep 2
    done
    exec hiveserver2
    ;;
  *)
    echo "Unsupported Hive role: $role" >&2
    exit 64
    ;;
esac
