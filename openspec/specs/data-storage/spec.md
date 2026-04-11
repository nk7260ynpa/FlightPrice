## MODIFIED Requirements

### Requirement: MySQL Docker 容器

系統 SHALL 透過 docker-compose 啟動 MySQL 容器，使用 Docker volume 持久化資料，並採用 mysql_native_password 認證方式。`flight_prices` 資料表 MUST 具有 `(flight_number, scrape_date)` 唯一約束，確保每日每班機僅存一筆價格紀錄。

#### Scenario: 容器啟動時自動建立資料表
- **WHEN** Docker 容器首次啟動
- **THEN** 系統自動建立 `flight_prices`、`tracked_flights`、`scrape_logs` 資料表

#### Scenario: 容器重啟後資料保留
- **WHEN** MySQL 容器重新啟動
- **THEN** 所有既有資料仍然存在，不會遺失

#### Scenario: 外部工具可正常連線
- **WHEN** 使用外部 MySQL 客戶端工具（DBeaver、DataGrip 等）透過主機 port 連線
- **THEN** 連線 SHALL 使用 mysql_native_password 認證，不出現 Public Key Retrieval 錯誤

#### Scenario: 每日每班機價格紀錄唯一
- **WHEN** 嘗試為同一班機在同一天寫入第二筆價格紀錄
- **THEN** 資料庫 SHALL 拒絕寫入並回傳唯一約束違反錯誤
