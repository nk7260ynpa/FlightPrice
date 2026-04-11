## MODIFIED Requirements

### Requirement: 從 Skyscanner 擷取航班價格

系統 SHALL 提供後台爬蟲服務，能擷取指定班機的價格資訊。當 SKYSCANNER_API_KEY 已設定時使用 Skyscanner API，未設定時使用 Playwright 爬取 Google Flights。擷取前 MUST 檢查當日是否已有該班機的價格紀錄，若已存在則跳過擷取。

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
