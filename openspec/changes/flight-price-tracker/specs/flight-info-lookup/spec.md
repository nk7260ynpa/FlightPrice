## ADDED Requirements

### Requirement: 根據班次代碼查詢航班資訊

系統 SHALL 提供航班資訊查詢功能，輸入班次代碼後自動回傳航空公司、出發地、抵達地。

#### Scenario: 成功查詢航班資訊
- **WHEN** 使用者輸入有效的班次代碼（例如 CI-100）
- **THEN** 系統回傳該班次的航空公司名稱、出發地 IATA 代碼、抵達地 IATA 代碼

#### Scenario: 查詢失敗或班次不存在
- **WHEN** 使用者輸入的班次代碼無法查詢到結果
- **THEN** 系統回傳錯誤訊息，提示使用者手動輸入航空公司、出發地、抵達地

### Requirement: 航班查詢 API 端點

系統 SHALL 提供 JSON API 端點供前端非同步呼叫，根據班次代碼查詢航班資訊。

#### Scenario: API 回傳航班資訊
- **WHEN** 前端以班次代碼呼叫查詢 API
- **THEN** API 回傳 JSON 包含 airline、origin、destination 欄位

#### Scenario: API 查詢無結果
- **WHEN** 前端以無效班次代碼呼叫查詢 API
- **THEN** API 回傳錯誤狀態與提示訊息
