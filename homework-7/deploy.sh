#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="${GRAFANA_NAMESPACE:-monitoring}"
RELEASE="${GRAFANA_RELEASE:-grafana}"
POSTGRES_DASHBOARD_URL="https://grafana.com/api/dashboards/9628/revisions/8/download"
POSTGRES_DASHBOARD_FILE="$(mktemp)"

cleanup() {
  rm -f "$POSTGRES_DASHBOARD_FILE"
}
trap cleanup EXIT

for command_name in kubectl helm curl jq; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Ошибка: требуется команда $command_name" >&2
    exit 1
  fi
done

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

kubectl create configmap grafana-dashboard-dormitory-helper \
  --namespace "$NAMESPACE" \
  --from-file=dormitory-helper.json="$SCRIPT_DIR/dashboard-dormitory-helper.json" \
  --dry-run=client -o yaml \
  | kubectl label --local -f - grafana_dashboard=1 -o yaml \
  | kubectl annotate --local -f - grafana_folder=DormitoryHelper -o yaml \
  | kubectl apply -f -

curl --fail --silent --show-error --location \
  "$POSTGRES_DASHBOARD_URL" \
  | jq '
      del(.__inputs)
      | .id = null
      | .uid = "postgresql-exporter"
      | .title = "PostgreSQL Exporter"
      | .templating.list |= map(
          if .name == "DS_PROMETHEUS" then
            .current = {"selected": true, "text": "VictoriaMetrics", "value": "victoriametrics"}
          else . end
        )
    ' > "$POSTGRES_DASHBOARD_FILE"

kubectl create configmap grafana-dashboard-postgresql \
  --namespace "$NAMESPACE" \
  --from-file=postgresql-exporter.json="$POSTGRES_DASHBOARD_FILE" \
  --dry-run=client -o yaml \
  | kubectl label --local -f - grafana_dashboard=1 -o yaml \
  | kubectl annotate --local -f - grafana_folder=PostgreSQL -o yaml \
  | kubectl apply -f -

helm repo add grafana-community https://grafana-community.github.io/helm-charts --force-update
helm repo update grafana-community
helm upgrade --install "$RELEASE" grafana-community/grafana \
  --namespace "$NAMESPACE" \
  --values "$SCRIPT_DIR/grafana-values.yml" \
  --wait \
  --timeout 5m

kubectl rollout status deployment/"$RELEASE" --namespace "$NAMESPACE" --timeout=180s

cat <<EOF

Grafana и оба дашборда установлены.

Открыть Grafana:
  kubectl port-forward service/$RELEASE 3000:80 --namespace $NAMESPACE

Адрес:  http://localhost:3000
Логин:  admin
Пароль: admin

Полная автоматическая проверка:
  $SCRIPT_DIR/verify.sh
EOF
