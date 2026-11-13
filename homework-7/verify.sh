#!/usr/bin/env bash
set -Eeuo pipefail

NAMESPACE="${GRAFANA_NAMESPACE:-monitoring}"
RELEASE="${GRAFANA_RELEASE:-grafana}"
VM_SERVICE="vectoriametrics-victoria-metrics-single-server"

echo "== Kubernetes resources =="
kubectl get pods,service,configmap --namespace "$NAMESPACE"

echo
echo "== Grafana health =="
kubectl get --raw \
  "/api/v1/namespaces/$NAMESPACE/services/http:$RELEASE:80/proxy/api/health"

echo
echo "== VictoriaMetrics datasource connectivity =="
kubectl get --raw \
  "/api/v1/namespaces/default/services/http:$VM_SERVICE:8428/proxy/health"

echo
echo "== Required metrics in VictoriaMetrics =="
for metric in \
  dormitory_helper_probe_success \
  http_requests_total \
  http_request_duration_seconds_bucket \
  process_resident_memory_bytes \
  pg_up; do
  result="$(kubectl get --raw \
    "/api/v1/namespaces/default/services/http:$VM_SERVICE:8428/proxy/api/v1/query?query=$metric")"
  if jq -e '.data.result | length > 0' >/dev/null <<<"$result"; then
    echo "OK  $metric"
  else
    echo "MISS $metric"
  fi
done

echo
echo "Ожидаются два dashboard ConfigMap:"
kubectl get configmap --namespace "$NAMESPACE" \
  --selector grafana_dashboard=1 \
  -o custom-columns=NAME:.metadata.name,FOLDER:.metadata.annotations.grafana_folder
