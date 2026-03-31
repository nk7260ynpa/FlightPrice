## MODIFIED Requirements

### Requirement: 選擇班機檢視價格圖表

系統 SHALL 提供下拉選單讓使用者選擇追蹤中的班機，選項 SHALL 包含班次代碼、航空公司、航線及出發日期。

#### Scenario: 下拉選單顯示出發日期
- **WHEN** 使用者開啟價格圖表頁面
- **THEN** 班機選擇下拉選單每個選項 SHALL 顯示出發日期，格式為 `班次代碼 (航空公司 出發地 → 抵達地) YYYY-MM-DD`

#### Scenario: 選擇班機後顯示圖表
- **WHEN** 使用者從下拉選單選擇一個班機
- **THEN** 頁面以折線圖呈現該班機的歷史票價變化
