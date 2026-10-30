#!/usr/bin/env sh

# Пример запуска: ./homework-5/demo-load.sh normal 60

BASE_URL="${BASE_URL:-http://localhost:8000}"
MODE="${1:-normal}"
COUNT="${2:-60}"

i=0
while [ "$i" -lt "$COUNT" ]; do
  curl --silent --output /dev/null \
    --write-out '%{http_code} %{time_total}\n' \
    "$BASE_URL/demo/work?mode=$MODE"
  i=$((i + 1))
done
