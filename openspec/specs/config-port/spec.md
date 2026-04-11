# config-port Specification

## Purpose

定義 FlightPrice Web 服務對外 port 的預設組態規格。

## Requirements

### Requirement: Web 服務預設 port 為 5003

系統 SHALL 將 Web 服務的預設對外 port 設定為 5003。

#### Scenario: 使用預設 port 啟動服務

- **WHEN** 使用者未自訂 `FLASK_PORT` 環境變數
- **THEN** Web 服務 SHALL 在 `localhost:5003` 提供存取

### Requirement: 服務須隨 Docker daemon 自動啟動

系統 SHALL 將 `db` 與 `web` 容器的 restart 政策設為 `always`，使其於 Docker daemon 啟動時自動拉起，且於異常終止時自動重啟。

#### Scenario: 主機重開機後服務自動啟動

- **WHEN** 主機重新開機且 Docker daemon 啟動完成
- **THEN** `flightprice-db` 與 `flightprice-web` 容器 SHALL 自動進入 running 狀態，無需手動執行 `run.sh`

#### Scenario: 容器異常崩潰後自動重啟

- **WHEN** `flightprice-web` 容器因例外而退出
- **THEN** Docker SHALL 自動重新啟動該容器
