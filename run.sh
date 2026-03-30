#!/bin/bash
#
# 啟動 FlightPrice 服務（MySQL + Flask 應用）

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly DOCKER_DIR="${SCRIPT_DIR}/docker"

# 確保 logs 資料夾存在
mkdir -p "${SCRIPT_DIR}/logs"

# 載入環境變數
if [[ -f "${SCRIPT_DIR}/.env" ]]; then
  set -a
  source "${SCRIPT_DIR}/.env"
  set +a
fi

# 啟動 Docker 容器
docker compose -f "${DOCKER_DIR}/docker-compose.yaml" up --build -d
