## Context

FlightPrice 使用 APScheduler 的 `BackgroundScheduler` 於應用啟動時註冊一個
`interval` 類型 job，每 3 小時執行 `scrape_all_active_flights()` 以擷取所有啟用
中的航班價格。實作位於 `app/scheduler.py`，啟動條件則由 `app/__init__.py`
的 `create_app()` 依 2026-04-23 已歸檔的 `fix-scheduler-double-trigger` 規格
控管。

使用者回報 3 小時間隔過於稀疏，希望改為 1 小時。此為單純常數調整，無架構
變更；但因為會使對外請求量增為 3 倍，仍值得以 design 文件記錄決策與風險
緩解方向。

## Goals / Non-Goals

**Goals：**

- 將排程任務 `periodic_scrape` 的觸發間隔由 `hours=3` 改為 `hours=1`。
- 讓文件、docstring、log 訊息與 spec 一致地描述新的 1 小時週期。
- 透過單元測試鎖定 job 間隔，避免日後誤改回舊值而無測試保護。

**Non-Goals：**

- 不改變排程器啟動條件邏輯（沿用 `fix-scheduler-double-trigger` 規格）。
- 不把間隔改為可配置（例如透過環境變數或設定檔），維持硬編碼常數。
- 不調整擷取邏輯、不做 rate limit／backoff；相關處理若必要，另立變更。
- 不變更 `BackgroundScheduler` 的 job store、executor 或 timezone 設定。

## Decisions

### 決策 1：使用 `hours=1` 而非 `minutes=60` 或 `cron`

- **選擇**：`scheduler.add_job(..., 'interval', hours=1, ...)`。
- **理由**：
  1. 與現行程式碼 `hours=3` 的形式最接近，diff 最小，審閱成本最低。
  2. `interval` trigger 與使用者需求（「每 1 小時」）語意一致；無需對齊
     整點。若未來需要整點觸發再改 `CronTrigger`。
- **替代方案**：
  - `minutes=60`：語意相同但可讀性較差。
  - `CronTrigger(hour='*')`：會對齊整點，行為與目前不同，超出本次需求。

### 決策 2：在 spec 新增獨立 Requirement，而非 MODIFY 既有 Requirement

- **選擇**：於 `specs/scheduler/spec.md` 以 `## ADDED Requirements` 新增一條
  「抓取週期為 1 小時」Requirement。
- **理由**：現有 Requirement 僅規範「啟動條件」，週期是正交關注點；以
  ADDED 新增可避免改動既有 scenarios、降低漏抄風險（見 `specs` 指令對
  MODIFIED 的警語）。

### 決策 3：測試以「檢查 job 的 `trigger.interval`」驗證

- **選擇**：新增測試呼叫 `init_scheduler`（以 fake/真實 Flask app 搭配
  `BackgroundScheduler` 但不 `start` 實際執行擷取），取出 `periodic_scrape`
  job 的 `trigger.interval` 與 `timedelta(hours=1)` 比較。
- **理由**：直接對應 spec 的可測試陳述；不依賴時間流逝、執行穩定。
- **替代方案**：
  - 解析原始碼字串：脆弱、易漏。
  - 端到端等待 1 小時：不可行。

## Risks / Trade-offs

- **Risk**：對外抓取頻率提升 3 倍，可能觸發航空公司網站 rate limit 或
  IP 封鎖 → **Mitigation**：本變更先觀察線上行為；若出現 429／失敗率
  飆升，另立變更加入 exponential backoff 或降頻開關。
- **Risk**：`price_history` 寫入量提升 3 倍，SQLite 長期可能膨脹 →
  **Mitigation**：目前資料量仍遠低於 SQLite 單檔舒適區；若日後需要，
  另立「歷史資料壓縮／歸檔」變更處理。
- **Trade-off**：硬編碼 1 小時便於測試與回滾，但每次調整都需改碼。可
  接受；若未來調整頻繁再做成設定項。
- **Risk**：測試若 `scheduler.start()` 了真的 BackgroundScheduler，會產生
  背景 thread 影響其他測試 → **Mitigation**：測試中 monkeypatch
  `BackgroundScheduler.start` 為 no-op，或使用 fixture 於 teardown 呼叫
  `scheduler.shutdown(wait=False)`。

## Migration Plan

1. 於 feature branch `opsx/adjust-fetch-interval-1h` 套用程式碼／測試／文件
   變更。
2. 本地執行 `./run.sh pytest` 或 `docker compose run --rm app pytest`，確認
   既有 `tests/test_app_factory.py` 與新增的間隔測試皆通過。
3. `/opsx:verify` 通過後 `/opsx:archive`，spec delta 自動同步至
   `openspec/specs/scheduler/spec.md`。
4. 部署：重啟 container（`run.sh` 流程）即套用新間隔。
5. **Rollback**：若線上出現 rate limit／異常，`git revert` 對應 merge commit
   即可回到 `hours=3`；因為無資料 schema 變更，無需資料遷移。

## Open Questions

- 無。若將來確認需要可設定化，再另立變更。
