#!/usr/bin/env bash
#
# 即時追蹤 FlightPrice Flask app 的 stdout 日誌。

set -euo pipefail

readonly NAMESPACE="flightprice"

main() {
  kubectl -n "${NAMESPACE}" logs -f deployment/flightprice-app "$@"
}

main "$@"
