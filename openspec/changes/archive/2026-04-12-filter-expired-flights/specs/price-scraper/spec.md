## MODIFIED Requirements

### Requirement: 從 Skyscanner 擷取航班價格

系統 SHALL 提供後台爬蟲服務，能擷取指定班機的價格資訊。當 SKYSCANNER_API_KEY 已設定時使用 Skyscanner API，未設定時使用 Playwright 爬取 Google Flights。擷取前 MUST 檢查當日是否已有該班機的價格紀錄，若已存在則跳過擷取。批次擷取時 MUST 排除出發日期已過的航班，僅對出發日期為今天或未來的啟用航班執行擷取。

#### Scenario: 有 API Key 時使用 Skyscanner API
- **WHEN** SKYSCANNER_API_KEY 環境變數已設定
- **THEN** 系統使用 Skyscanner Partners API 擷取價格

#### Scenario: 無 API Key 時使用 Google Flights 網頁爬取
- **WHEN** SKYSCANNER_API_KEY 環境變數未設定
- **THEN** 系統使用 Playwright headless browser 開啟 Google Flights 搜尋頁面，以 `[data-gs]` 選擇器擷取所有價格，取最低價寫入資料庫

#### Scenario: 成功擷取價格
- **WHEN** 爬蟲對 tracked_flights 中的啟用班機執行價格擷取
- **THEN** 系統取得該航線的最低價格並寫入 `flight_prices` 表

#### Scenario: 網頁爬取失敗處理
- **WHEN** Playwright 爬取超時或頁面無法載入價格
- **THEN** 系統記錄錯誤日誌，不中斷其他班機的擷取流程

#### Scenario: 當日已有該班機資料時跳過擷取
- **WHEN** `flight_prices` 表中已存在該班機當日的價格紀錄
- **THEN** 系統 SHALL 跳過該班機的擷取，不產生重複紀錄

#### Scenario: 出發日期已過的航班不進行擷取
- **WHEN** 批次擷取所有啟用航班時，某航班的 `departure_date` 早於今天
- **THEN** 系統 SHALL 在查詢階段排除該航班，不對其發起任何擷取動作
