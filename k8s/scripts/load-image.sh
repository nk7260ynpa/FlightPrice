#!/usr/bin/env bash
#
# 將本機 daemon 內的 flightprice-app:latest image 載入 Docker Desktop
# Kubernetes 的 kind 節點。
#
# 為何需要這支腳本：
# 新版 Docker Desktop Kubernetes 採 kind 多節點架構（desktop-control-plane
# + desktop-worker），節點內的 containerd 與 host docker daemon 是隔離的。
# host 端 `docker build` 出的 image 不會自動進到 K8s 節點，必須透過 kind
# 工具明確 load。
#
# 前置：請先 `brew install kind`（macOS）。

set -euo pipefail

readonly IMAGE="${IMAGE:-flightprice-app:latest}"

err() {
  echo "[ERROR] $*" >&2
}

info() {
  echo "[INFO] $*"
}

main() {
  if ! command -v kind >/dev/null 2>&1; then
    err "未安裝 kind。請先執行：brew install kind"
    err "（kind 是將本機 image 載入 Docker Desktop K8s 節點所需的官方工具）"
    exit 1
  fi

  if ! docker image inspect "${IMAGE}" >/dev/null 2>&1; then
    err "本機找不到 image：${IMAGE}"
    err "請先執行：./docker/build.sh"
    exit 1
  fi

  local cluster
  cluster="$(kind get clusters 2>/dev/null | grep -m1 -E '^desktop$' || true)"
  if [[ -z "${cluster}" ]]; then
    # 退而求其次：抓第一個 kind cluster
    cluster="$(kind get clusters 2>/dev/null | head -n1 || true)"
  fi

  if [[ -z "${cluster}" ]]; then
    err "找不到任何 kind cluster。請確認 Docker Desktop Kubernetes 已啟動。"
    exit 1
  fi

  info "載入 ${IMAGE} 至 kind cluster：${cluster}"
  kind load docker-image "${IMAGE}" --name "${cluster}"
  info "完成。"
}

main "$@"
