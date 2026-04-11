## Why

目前 `docker-compose.yaml` 中 MySQL 與 Flask Web 容器的 `restart` 政策為 `unless-stopped`，若使用者曾手動 `docker stop` 停止容器，重開機後 Docker daemon 啟動時不會自動拉起這些服務。為確保機器開機後 FlightPrice 服務皆能自動啟動並持續提供追蹤與擷取功能，需將重啟政策調整為「總是自動啟動」。

## What Changes

- 將 `docker/docker-compose.yaml` 中 `db` 與 `web` 服務的 `restart` 政策由 `unless-stopped` 改為 `always`
- 更新 README.md 的「安裝與啟動」段落，說明服務會隨 Docker daemon 自動啟動
- 不影響既有 build、啟動指令或環境變數

## Capabilities

### New Capabilities
（無）

### Modified Capabilities
- `config-port`：此 capability 目前涵蓋 docker-compose 服務設定；新增「服務須隨 Docker daemon 自動啟動」的需求

## Impact

- 影響檔案：`docker/docker-compose.yaml`、`README.md`
- 影響系統：Docker daemon 啟動時會自動拉起 `flightprice-db` 與 `flightprice-web` 容器
- 無 API、依賴套件或資料庫 schema 變更
