#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

kubectl apply -f "$SCRIPT_DIR/k8s/alert-webhook.yml"
kubectl apply -f "$SCRIPT_DIR/k8s/alertmanager.yml"
kubectl apply -f "$SCRIPT_DIR/k8s/vmalert.yml"

kubectl rollout status deployment/alert-webhook --timeout=180s
kubectl rollout status deployment/alertmanager --timeout=180s
kubectl rollout status deployment/vmalert --timeout=180s

cat <<'EOF'

Стек алертинга запущен.

Интерфейс vmalert:
  kubectl port-forward service/vmalert 8880:8880

Интерфейс Alertmanager:
  kubectl port-forward service/alertmanager 9093:9093

Полученные webhook-уведомления:
  kubectl port-forward service/alert-webhook 8080:8080
EOF
