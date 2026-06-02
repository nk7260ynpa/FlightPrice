#!/usr/bin/env bash
#
# 完全清除 FlightPrice 在 K8s 上的所有資源（含 PVC 與 namespace）。
# 警告：MySQL 資料與 logs 都會被刪除，無法復原。

set -euo pipefail

readonly NAMESPACE="flightprice"

info() {
  echo "[INFO] $*"
}

warn() {
  echo "[WARN] $*" >&2
}

main() {
  if ! kubectl get namespace "${NAMESPACE}" >/dev/null 2>&1; then
    info "namespace ${NAMESPACE} 不存在，無需清除。"
    return 0
  fi

  warn "即將刪除 namespace ${NAMESPACE} 連同所有資源（含 PVC）。"
  read -r -p "確定繼續？輸入 'yes' 確認：" confirm
  if [[ "${confirm}" != "yes" ]]; then
    info "已取消。"
    return 0
  fi

  info "刪除 namespace ${NAMESPACE}（含 PVC）..."
  kubectl delete namespace "${NAMESPACE}" --wait=true
  info "清除完成。"
}

main "$@"
