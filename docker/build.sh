#!/bin/bash
#
# 建立 FlightPrice Docker image

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"

docker build -t flightprice-app -f "${SCRIPT_DIR}/Dockerfile" "${PROJECT_DIR}"
