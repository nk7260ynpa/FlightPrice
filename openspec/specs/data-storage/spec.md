## MODIFIED Requirements

### Requirement: MySQL Docker 容器

系統 SHALL 透過 docker-compose 啟動 MySQL 容器，使用 Docker volume 持久化資料，並採用 mysql_native_password 認證方式。

#### Scenario: 容器啟動時自動建立資料表
- **WHEN** Docker 容器首次啟動
- **THEN** 系統自動建立 `flight_prices`、`tracked_flights`、`scrape_logs` 資料表

#### Scenario: 容器重啟後資料保留
- **WHEN** MySQL 容器重新啟動
- **THEN** 所有既有資料仍然存在，不會遺失

#### Scenario: 外部工具可正常連線
- **WHEN** 使用外部 MySQL 客戶端工具（DBeaver、DataGrip 等）透過主機 port 連線
- **THEN** 連線 SHALL 使用 mysql_native_password 認證，不出現 Public Key Retrieval 錯誤
