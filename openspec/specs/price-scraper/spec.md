## ADDED Requirements

### Requirement: 從 Skyscanner 擷取航班價格

系統 SHALL 提供後台爬蟲服務，能從 Skyscanner 擷取指定班機的價格資訊。

#### Scenario: 成功擷取價格
- **WHEN** 爬蟲對 tracked_flights 中的啟用班機執行價格擷取
- **THEN** 系統從 Skyscanner 取得該班機的價格、出發時間、航空公司、出發地、抵達地，並寫入 `flight_prices` 表

#### Scenario: 擷取失敗處理
- **WHEN** 擷取某班機價格時發生錯誤（網路逾時、API 回應異常等）
- **THEN** 系統記錄錯誤日誌，不中斷其他班機的擷取流程

### Requirement: 每日定時執行擷取

系統 SHALL 每日自動執行一次價格擷取，遍歷所有啟用追蹤的班機。

#### Scenario: 定時觸發擷取
- **WHEN** 到達每日設定的擷取時間
- **THEN** 系統自動對所有 `is_active = TRUE` 的 tracked_flights 執行價格擷取

#### Scenario: 僅擷取啟用的班機
- **WHEN** 某班機的 `is_active` 為 FALSE
- **THEN** 系統跳過該班機，不進行價格擷取

### Requirement: 抓取狀態紀錄

系統 SHALL 記錄每次擷取的狀態（成功/失敗）與時間戳記。

#### Scenario: 記錄成功擷取
- **WHEN** 成功擷取某班機的價格
- **THEN** 系統記錄該班機的擷取狀態為「成功」及擷取時間

#### Scenario: 記錄失敗擷取
- **WHEN** 擷取某班機的價格失敗
- **THEN** 系統記錄該班機的擷取狀態為「失敗」、錯誤原因及擷取時間
