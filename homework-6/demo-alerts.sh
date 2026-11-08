#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"
DURATION_SECONDS="${DURATION_SECONDS:-120}"

usage() {
  cat <<'EOF'
Использование:
  ./homework-6/demo-alerts.sh errors        # поток 503 для HighHttp5xxRate
  ./homework-6/demo-alerts.sh slow          # медленные параллельные запросы
  ./homework-6/demo-alerts.sh unavailable   # временно остановить PostgreSQL

Для режимов errors и slow сначала выполните:
  kubectl port-forward service/backend 8000:8000

Продолжительность можно изменить:
  DURATION_SECONDS=150 ./homework-6/demo-alerts.sh errors
EOF
}

load() {
  local mode="$1"
  local concurrency="$2"
  local end_time=$((SECONDS + DURATION_SECONDS))
  if ! curl --silent --fail --output /dev/null "$BASE_URL/health/live"; then
    echo "Backend недоступен по адресу $BASE_URL. Запустите kubectl port-forward service/backend 8000:8000." >&2
    exit 1
  fi
  echo "Генерирую mode=$mode, concurrency=$concurrency, duration=${DURATION_SECONDS}s"
  while (( SECONDS < end_time )); do
    local pids=()
    for ((i = 0; i < concurrency; i++)); do
      curl --silent --output /dev/null \
        "$BASE_URL/demo/work?mode=$mode" &
      pids+=("$!")
    done
    for pid in "${pids[@]}"; do
      wait "$pid" || true
    done
  done
  echo "Нагрузка завершена. Подождите до 30 секунд доставки уведомления."
}

unavailable() {
  local replicas
  replicas="$(kubectl get deployment postgres -o jsonpath='{.spec.replicas}')"
  if [[ -z "$replicas" ]]; then
    replicas=1
  fi
  restore() {
    echo "Восстанавливаю PostgreSQL: replicas=$replicas"
    kubectl scale deployment/postgres --replicas="$replicas"
  }
  trap restore EXIT
  kubectl scale deployment/postgres --replicas=0
  echo "PostgreSQL остановлен на ${DURATION_SECONDS}s для срабатывания алерта."
  sleep "$DURATION_SECONDS"
}

case "${1:-}" in
  errors) load error 10 ;;
  slow) load slow 20 ;;
  unavailable) unavailable ;;
  *) usage; exit 1 ;;
esac
