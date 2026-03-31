## ADDED Requirements

### Requirement: flight_prices 資料表

系統 SHALL 建立 `flight_prices` 資料表，包含以下欄位：
- `id`：主鍵，自動遞增
- `flight_number`：班次編號（VARCHAR）
- `price`：票價（DECIMAL）
- `scrape_date`：抓取價格的日期（DATE）
- `departure_time`：出發時間（DATETIME）
- `airline`：航空公司名稱（VARCHAR）
- `origin`：出發地（VARCHAR）
- `destination`：抵達地（VARCHAR）
- `created_at`：紀錄建立時間（DATETIME）

#### Scenario: 成功儲存航班價格紀錄
- **WHEN** 爬蟲成功擷取一筆航班價格資料
- **THEN** 系統將該筆資料寫入 `flight_prices` 表，所有欄位皆正確儲存

#### Scenario: 同一班次同一天多次抓取
- **WHEN** 同一班次在同一天被多次抓取
- **THEN** 系統為每次抓取建立獨立紀錄，不覆蓋既有資料

### Requirement: tracked_flights 資料表

系統 SHALL 建立 `tracked_flights` 資料表，包含以下欄位：
- `id`：主鍵，自動遞增
- `flight_number`：班次編號（VARCHAR）
- `airline`：航空公司名稱（VARCHAR）
- `origin`：出發地（VARCHAR）
- `destination`：抵達地（VARCHAR）
- `departure_date`：出發日期（DATE，必填）
- `is_active`：是否啟用追蹤（BOOLEAN，預設 TRUE）
- `created_at`：紀錄建立時間（DATETIME）

#### Scenario: 新增追蹤班機
- **WHEN** 使用者新增一筆追蹤班機
- **THEN** 系統在 `tracked_flights` 表建立紀錄，`is_active` 預設為 TRUE

#### Scenario: 防止重複追蹤
- **WHEN** 使用者嘗試新增已存在的班次編號
- **THEN** 系統拒絕新增並回傳錯誤訊息

### Requirement: MySQL Docker 容器

系統 SHALL 透過 docker-compose 啟動 MySQL 容器，並使用 Docker volume 持久化資料。

#### Scenario: 容器啟動時自動建立資料表
- **WHEN** Docker 容器首次啟動
- **THEN** 系統自動建立 `flight_prices` 與 `tracked_flights` 資料表

#### Scenario: 容器重啟後資料保留
- **WHEN** MySQL 容器重新啟動
- **THEN** 所有既有資料仍然存在，不會遺失
