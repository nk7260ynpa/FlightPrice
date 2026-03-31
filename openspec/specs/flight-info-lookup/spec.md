## ADDED Requirements

### Requirement: 多層備援航班資訊查詢

系統 SHALL 提供四層備援的航班資訊查詢功能，依序嘗試直到取得航空公司、出發地、抵達地。

#### Scenario: DB 快取命中
- **WHEN** 使用者輸入班次代碼且 tracked_flights 表中已有同班次紀錄
- **THEN** 系統直接複製既有紀錄的 airline、origin、destination 回傳，不發起外部請求

#### Scenario: Flightradar24 爬取成功
- **WHEN** DB 無快取，且 Flightradar24 網頁可正常存取
- **THEN** 系統從 Flightradar24 爬取該班次的航空公司、出發地 IATA 代碼、抵達地 IATA 代碼

#### Scenario: Flightradar24 失敗，AviationStack 成功
- **WHEN** Flightradar24 爬取失敗（反爬蟲阻擋、網路錯誤等），且 AviationStack API Key 已設定
- **THEN** 系統改從 AviationStack API 查詢並回傳完整航班資訊

#### Scenario: 僅 IATA 代碼對照表可用
- **WHEN** 前三層查詢皆失敗
- **THEN** 系統從班次代碼前綴解析航空公司名稱，出發地與抵達地回傳空值，提示使用者手動輸入

#### Scenario: 所有查詢皆失敗
- **WHEN** 班次代碼無法匹配任何資料來源
- **THEN** 系統回傳錯誤訊息，所有欄位開放手動輸入

### Requirement: Flightradar24 爬取模組

系統 SHALL 透過 HTTP 請求爬取 Flightradar24 航班頁面，解析出航線資訊。

#### Scenario: 正常爬取
- **WHEN** 系統對 Flightradar24 發起 HTTP 請求
- **THEN** 請求 SHALL 包含模擬瀏覽器的 User-Agent header，並設定合理的 timeout

#### Scenario: 被反爬蟲機制阻擋
- **WHEN** Flightradar24 回傳非 200 狀態碼或無法解析內容
- **THEN** 系統記錄警告日誌並降級至下一層查詢

### Requirement: 航班查詢 API 端點

系統 SHALL 提供 JSON API 端點供前端非同步呼叫，根據班次代碼查詢航班資訊。

#### Scenario: API 回傳航班資訊
- **WHEN** 前端以班次代碼呼叫查詢 API
- **THEN** API 回傳 JSON 包含 airline、origin、destination 欄位

#### Scenario: API 查詢無結果
- **WHEN** 前端以無效班次代碼呼叫查詢 API
- **THEN** API 回傳錯誤狀態與提示訊息
