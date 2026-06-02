#!/usr/bin/env bash
#
# 部署 FlightPrice 至本機 Docker Desktop Kubernetes。
#
# 流程：
#   1. 檢查必要工具與 .env 必要欄位。
#   2. 從 .env 動態產生 flightprice-secret（不入 git）。
#   3. 套用 Kustomize overlay。
#   4. 等待 pods Ready。

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly K8S_DIR="$(dirname "${SCRIPT_DIR}")"
readonly PROJECT_DIR="$(dirname "${K8S_DIR}")"
readonly ENV_FILE="${PROJECT_DIR}/.env"
readonly NAMESPACE="flightprice"
readonly OVERLAY="${K8S_DIR}/overlays/docker-desktop"

# 必須存在於 .env 的欄位
readonly REQUIRED_KEYS=(
  "MYSQL_ROOT_PASSWORD"
  "MYSQL_DATABASE"
  "MYSQL_USER"
  "MYSQL_PASSWORD"
)

err() {
  echo "[ERROR] $*" >&2
}

info() {
  echo "[INFO] $*"
}

check_prerequisites() {
  if ! command -v kubectl >/dev/null 2>&1; then
    err "未安裝 kubectl"
    exit 1
  fi

  if [[ ! -f "${ENV_FILE}" ]]; then
    err ".env 不存在：${ENV_FILE}"
    err "請先複製 .env.example 並填入實際值。"
    exit 1
  fi

  local missing=()
  for key in "${REQUIRED_KEYS[@]}"; do
    if ! grep -qE "^${key}=.+" "${ENV_FILE}"; then
      missing+=("${key}")
    fi
  done

  if [[ "${#missing[@]}" -gt 0 ]]; then
    err ".env 缺少必要欄位：${missing[*]}"
    exit 1
  fi

  if ! docker image inspect flightprice-app:latest >/dev/null 2>&1; then
    err "本機找不到 image：flightprice-app:latest"
    err "請先執行：./docker/build.sh"
    exit 1
  fi
}

load_image_into_kind() {
  # Docker Desktop K8s 自 4.x 起改為 kind 多節點架構，host daemon 的 image
  # 不會自動進入節點。若偵測到 kind cluster，必須先 load image。
  if kubectl get nodes -o name 2>/dev/null | grep -q "^node/desktop-"; then
    info "偵測到 Docker Desktop kind cluster，載入 image 至節點..."
    "${SCRIPT_DIR}/load-image.sh"
  fi
}

ensure_namespace() {
  if ! kubectl get namespace "${NAMESPACE}" >/dev/null 2>&1; then
    info "建立 namespace ${NAMESPACE}"
    kubectl create namespace "${NAMESPACE}"
  fi
}

apply_secret() {
  info "從 .env 產生 Secret：flightprice-secret"
  kubectl -n "${NAMESPACE}" create secret generic flightprice-secret \
    --from-env-file="${ENV_FILE}" \
    --dry-run=client -o yaml | kubectl apply -f -
}

apply_manifests() {
  info "套用 Kustomize overlay：${OVERLAY}"
  kubectl apply -k "${OVERLAY}"
}

wait_for_ready() {
  info "等待 MySQL 與 Flask pods Ready（最多 5 分鐘）..."
  kubectl -n "${NAMESPACE}" rollout status statefulset/mysql --timeout=300s
  kubectl -n "${NAMESPACE}" rollout status deployment/flightprice-app --timeout=300s
}

print_next_steps() {
  cat <<EOF

部署完成！後續操作：
  - 看 log：       ./k8s/scripts/logs.sh
  - 開放本機 5003：./k8s/scripts/port-forward.sh
  - 拆掉但保留資料：./k8s/scripts/teardown.sh
  - 全部清掉：     ./k8s/scripts/purge.sh
EOF
}

main() {
  check_prerequisites
  ensure_namespace
  apply_secret
  load_image_into_kind
  apply_manifests
  wait_for_ready
  print_next_steps
}

main "$@"
