## ADDED Requirements

### Requirement: 強制抓取所有啟用班機

系統 SHALL 提供強制抓取函式，對所有啟用班機執行價格擷取，不受當日資料檢查限制。

#### Scenario: 強制抓取成功
- **WHEN** 呼叫強制抓取函式
- **THEN** 系統對所有 `is_active = TRUE` 的班機執行價格擷取，不論當日是否已有資料

#### Scenario: 強制抓取回傳結果
- **WHEN** 強制抓取完成
- **THEN** 回傳成功與失敗的數量統計
