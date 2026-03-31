## MODIFIED Requirements

### Requirement: 從 Skyscanner 擷取航班價格

系統 SHALL 提供後台爬蟲服務，能從 Skyscanner 擷取指定班機的價格資訊。當 SKYSCANNER_API_KEY 已設定時使用 API，未設定時使用 Playwright 網頁爬取。

#### Scenario: 有 API Key 時使用 API
- **WHEN** SKYSCANNER_API_KEY 環境變數已設定
- **THEN** 系統使用 Skyscanner Partners API 擷取價格（原有邏輯）

#### Scenario: 無 API Key 時使用網頁爬取
- **WHEN** SKYSCANNER_API_KEY 環境變數未設定
- **THEN** 系統使用 Playwright headless browser 開啟 Skyscanner 搜尋頁面，等待價格載入後解析最低價

#### Scenario: 成功擷取價格
- **WHEN** 爬蟲對 tracked_flights 中的啟用班機執行價格擷取
- **THEN** 系統取得該航線的最低價格並寫入 `flight_prices` 表

#### Scenario: 網頁爬取失敗處理
- **WHEN** Playwright 爬取超時或頁面無法載入價格
- **THEN** 系統記錄錯誤日誌，不中斷其他班機的擷取流程

#### Scenario: 擷取失敗處理
- **WHEN** 擷取某班機價格時發生錯誤（網路逾時、反爬蟲阻擋等）
- **THEN** 系統記錄錯誤日誌，不中斷其他班機的擷取流程
