#!/usr/bin/env bash
#
# 拆除 FlightPrice 工作負載但保留 PVC（資料庫與 logs 內容保留）。

set -euo pipefail

readonly NAMESPACE="flightprice"

info() {
  echo "[INFO] $*"
}

main() {
  if ! kubectl get namespace "${NAMESPACE}" >/dev/null 2>&1; then
    info "namespace ${NAMESPACE} 不存在，無需拆除。"
    return 0
  fi

  info "刪除 Deployment、StatefulSet、Service、ConfigMap、Secret..."
  # 明確列出要刪除的資源類型，避免 kubectl delete -k 連 namespace 一併刪除
  # 而造成 PVC 被 cascade 清掉。
  kubectl -n "${NAMESPACE}" delete deployment,statefulset,service,configmap,secret --all \
    --ignore-not-found=true

  info "PVC 已保留，再次執行 deploy.sh 可恢復資料："
  kubectl -n "${NAMESPACE}" get pvc 2>/dev/null || true
}

main "$@"
