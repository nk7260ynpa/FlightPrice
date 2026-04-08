## ADDED Requirements

### Requirement: 服務須隨 Docker daemon 自動啟動

系統 SHALL 將 `db` 與 `web` 容器的 restart 政策設為 `always`，使其於 Docker daemon 啟動時自動拉起，且於異常終止時自動重啟。

#### Scenario: 主機重開機後服務自動啟動

- **WHEN** 主機重新開機且 Docker daemon 啟動完成
- **THEN** `flightprice-db` 與 `flightprice-web` 容器 SHALL 自動進入 running 狀態，無需手動執行 `run.sh`

#### Scenario: 容器異常崩潰後自動重啟

- **WHEN** `flightprice-web` 容器因例外而退出
- **THEN** Docker SHALL 自動重新啟動該容器
