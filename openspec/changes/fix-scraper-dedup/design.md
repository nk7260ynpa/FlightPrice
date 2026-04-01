## Context

目前 `scrape_all_active_flights()` 已在應用層檢查當日是否有資料，但 `force_scrape_all_active_flights()` 繞過此檢查。且 `flight_prices` 資料表無 `(flight_number, scrape_date)` 唯一約束，無法在 DB 層面防止重複。

現有流程：
- 排程每 3 小時呼叫 `scrape_all_active_flights()` → 有去重
- 手動強制擷取呼叫 `force_scrape_all_active_flights()` → 無去重
- `scrape_flight_price()` 底層函式不做去重判斷

## Goals / Non-Goals

**Goals:**
- 確保所有擷取路徑都執行去重檢查（包含強制擷取）
- 在資料庫層面加上唯一約束，防止 race condition 導致重複
- 保持程式碼簡潔，消除重複邏輯

**Non-Goals:**
- 不修改 Skyscanner API 或 Playwright 爬取邏輯
- 不處理既有重複資料的清理（專案仍在初始階段，無生產資料）

## Decisions

### 決策 1：統一去重邏輯位置

**選擇**：將去重檢查移至 `scrape_flight_price()` 底層函式，上層函式不再各自判斷。

**替代方案**：
- 在 `force_scrape_all_active_flights()` 複製去重邏輯 → 重複程式碼，維護成本高
- 移除 `force_scrape_all_active_flights()` → 失去手動觸發的能力（但實際上去重後行為等同）

**理由**：去重是核心業務規則（每日每班機一筆），應在最底層保證。上層只需負責「擷取哪些班機」。`force_scrape_all_active_flights()` 可移除，因為去重後其行為與 `scrape_all_active_flights()` 完全相同。

### 決策 2：資料庫唯一約束

**選擇**：在 FlightPrice 模型加上 `UniqueConstraint('flight_number', 'scrape_date')`。

**替代方案**：
- 使用 `(tracked_flight_id, scrape_date)` → tracked_flight_id 可為 null，唯一約束對 null 不可靠
- 不加約束，僅靠應用層 → 並發時可能出現重複

**理由**：`flight_number` + `scrape_date` 是業務上的自然唯一鍵，且兩欄位皆非 null。

## Risks / Trade-offs

- **[風險] 既有重複資料導致 migration 失敗** → 專案處於初始階段，無生產資料。若有測試資料需先清理再加約束。
- **[取捨] 移除 force_scrape 函式** → 失去「跳過去重」的手動能力，但這正是我們要消除的行為。若未來需要更新當日價格，應改用 upsert 機制而非允許重複。
