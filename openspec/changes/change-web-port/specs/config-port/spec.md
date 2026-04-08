## ADDED Requirements

### Requirement: Web 服務預設 port 為 5002

系統 SHALL 將 Web 服務的預設對外 port 設定為 5002。

#### Scenario: 使用預設 port 啟動服務

- **WHEN** 使用者未自訂 `FLASK_PORT` 環境變數
- **THEN** Web 服務 SHALL 在 `localhost:5002` 提供存取
