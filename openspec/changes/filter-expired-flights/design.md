## Context

目前 `scrape_all_active_flights()` 使用 `TrackedFlight.query.filter_by(is_active=True)` 查詢待爬取航班，沒有檢查出發日期。當航班出發日期已過（如 TR874 的 2026-03-28），Playwright 仍會嘗試爬取 Google Flights，因頁面不顯示過去日期價格而超時失敗。

## Goals / Non-Goals

**Goals:**

- 在查詢階段排除出發日期已過的航班，避免無效爬取
- 保持 `is_active` 欄位語意不變，讓使用者仍可手動管理航班啟停

**Non-Goals:**

- 不自動將過期航班的 `is_active` 設為 `False`
- 不修改單筆爬取函式 `scrape_flight_price()` 的邏輯
- 不處理「當天出發」的邊界案例（當天仍可查詢價格）

## Decisions

### 在查詢層過濾，不在爬取層過濾

在 `scrape_all_active_flights()` 的 ORM 查詢中加入 `TrackedFlight.departure_date >= date.today()` 條件。

**替代方案**：在 `scrape_flight_price()` 開頭檢查日期後提前返回。
**選擇理由**：查詢層過濾更高效，不需實例化 TrackedFlight 物件，也不會啟動 Playwright。從資料庫端直接排除，語意更清晰。

### 不修改 is_active 狀態

過期航班僅在爬取查詢時被過濾，`is_active` 保持不變。

**替代方案**：排程中自動將過期航班設為 `is_active=False`。
**選擇理由**：`is_active` 是使用者控制的欄位。若使用者想更新出發日期後繼續追蹤同一班機，自動停用會造成困擾。查詢過濾能達到同樣效果且無副作用。

## Risks / Trade-offs

- **[過期航班仍顯示為「啟用」]** → 使用者在管理頁面看到已過期但仍 active 的航班可能困惑。日後可考慮在 UI 加上過期標示，但不在本次範圍。
- **[時區差異]** → `date.today()` 使用容器時區（已設為 Asia/Taipei），與使用者預期一致，風險低。
