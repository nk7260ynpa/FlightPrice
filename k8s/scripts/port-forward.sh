#!/usr/bin/env bash
#
# 將 cluster 內 svc/flightprice-app:5000 轉發到本機 5003。
# 對齊 docker-compose 預設的對外 port。

set -euo pipefail

readonly NAMESPACE="flightprice"
readonly LOCAL_PORT="${LOCAL_PORT:-5003}"
readonly SVC_PORT="5000"

info() {
  echo "[INFO] $*"
}

main() {
  info "port-forward svc/flightprice-app: localhost:${LOCAL_PORT} -> svc:${SVC_PORT}"
  info "按 Ctrl-C 結束。"
  kubectl -n "${NAMESPACE}" port-forward "svc/flightprice-app" "${LOCAL_PORT}:${SVC_PORT}"
}

main "$@"
