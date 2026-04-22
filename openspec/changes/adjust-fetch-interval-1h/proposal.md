# Proposal: adjust-fetch-interval-1h

## Why

目前排程器（`app/scheduler.py`）每 3 小時才執行一次航班價格擷取，使用者希望提高抓取頻率以獲得更即時的價格變化觀測與更細緻的歷史資料。將間隔調整為 1 小時可在不引入新技術元件的前提下，將單日抓取次數由 8 次提升至 24 次。

## What Changes

- 將 `app/scheduler.py` 中 `scheduler.add_job(..., 'interval', hours=3, ...)` 參數由 `hours=3` 改為 `hours=1`。
- 同步更新模組 docstring、`init_scheduler` 的 docstring 與啟動時的 logger 訊息，將「每 3 小時」改為「每 1 小時」。
- 同步更新 `README.md` 中描述 APScheduler 排程的段落（若有提及週期）。
- 更新 `openspec/specs/scheduler/spec.md`：新增一條 Requirement，明確規範抓取週期為 1 小時（MODIFIED delta）。
- 調整／新增單元測試，驗證排程任務的 `interval` 設定為 1 小時（而非 3 小時），並確保既有排程啟動條件的測試仍通過。

不包含（out of scope）：
- 不改變既有的啟動條件邏輯（TESTING / debug / WERKZEUG_RUN_MAIN）。
- 不改變 `scrape_all_active_flights` 內部實作。
- 不引入 cron 類型排程、不調整 `BackgroundScheduler` 以外的排程機制。
- 不新增動態設定（例如從環境變數讀取間隔），仍維持硬編碼常數；若未來需要可另立變更。

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `scheduler`: 既有 spec 僅規範啟動條件；本次新增「抓取週期為 1 小時」的 Requirement，作為排程行為的第二條不變式（invariant）。

## Impact

- **程式碼**：`app/scheduler.py`（單一檔案，僅常數與文字變更）。
- **測試**：`tests/` 下新增或修改一個測試檔，驗證 job 的 `trigger.interval` 為 1 小時。
- **文件**：`README.md`（若敘述週期）、`openspec/specs/scheduler/spec.md`（透過 archive 同步）。
- **執行期影響**：單日抓取次數由 8 次 → 24 次，外部航空公司 API／網站請求量增加 3 倍；目前尚無速率限制紀錄，評估為低風險；若未來出現 429/封鎖，需另立變更加入 backoff 或降頻策略。
- **資料量**：`price_history` 寫入量同步增加 3 倍，短期內仍在 SQLite 可負荷範圍。
- **相容性**：不涉及介面變動，無 breaking change；既有資料與 API 不受影響。
- **回滾策略**：改回 `hours=3` 並回復 docstring／log／spec，單 commit 可回滾。
