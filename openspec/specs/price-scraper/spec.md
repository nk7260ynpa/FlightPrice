## MODIFIED Requirements

### Requirement: 每日定時執行擷取

系統 SHALL 每 3 小時自動檢查並執行價格擷取，僅對當日尚無價格資料的啟用班機執行爬蟲。

#### Scenario: 定時觸發檢查
- **WHEN** 每 3 小時排程觸發
- **THEN** 系統檢查所有 `is_active = TRUE` 的 tracked_flights，查詢 flight_prices 表是否有 `scrape_date = 今日` 的紀錄

#### Scenario: 當日無資料時執行爬蟲
- **WHEN** 某啟用班機在 flight_prices 表中無 `scrape_date = 今日` 的紀錄
- **THEN** 系統對該班機執行價格擷取

#### Scenario: 當日已有資料時跳過
- **WHEN** 某啟用班機在 flight_prices 表中已有 `scrape_date = 今日` 的紀錄
- **THEN** 系統跳過該班機，不進行重複擷取

#### Scenario: 僅擷取啟用的班機
- **WHEN** 某班機的 `is_active` 為 FALSE
- **THEN** 系統跳過該班機，不進行價格擷取
