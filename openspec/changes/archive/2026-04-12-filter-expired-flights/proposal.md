## Why

爬蟲排程每 3 小時對所有 `is_active=True` 的航班執行價格擷取，但未檢查出發日期是否已過。當航班出發日期已過（如 TR874 的 2026-03-28），Google Flights 不會顯示該日期的價格，導致每次爬取都超時失敗，白白消耗 Playwright 資源與時間。

## What Changes

- 在 `scrape_all_active_flights()` 查詢啟用航班時，加入 `departure_date >= today` 條件，排除出發日期已過的航班
- 過期航班不會被自動停用（`is_active` 不變），保留使用者手動管理的彈性；僅在爬取時過濾

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `price-scraper`: 新增「出發日期已過的航班不進行擷取」的行為規則

## Impact

- **程式碼**: `app/scraper.py` — `scrape_all_active_flights()` 函式的資料庫查詢條件
- **測試**: `tests/test_scraper.py` — 新增過期航班過濾的測試案例
- **行為變化**: 出發日期已過的航班仍保持 `is_active=True`，但不會被爬蟲排程選取執行
