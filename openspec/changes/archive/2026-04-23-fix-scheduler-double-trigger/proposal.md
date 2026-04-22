# Proposal: fix-scheduler-double-trigger

## Intent（意圖）

修復 Flask debug 模式下 APScheduler 被重複觸發的 bug。當 `FLASK_DEBUG=1`
時，Werkzeug auto-reloader 會同時存在 parent 與 child 兩個 process，兩者皆會
呼叫 `create_app()` → `init_scheduler(app)`，各自啟動一個 `BackgroundScheduler`，
導致同一排程 job 在同一秒被觸發兩次，兩組 worker 競爭寫入 `flight_prices`
資料表並觸發 `uq_flight_scrape_date` 唯一鍵衝突，log 中出現大量
`IntegrityError: Duplicate entry` 錯誤。

## Scope（範圍）

### 會改動的模組

- `app/__init__.py`：調整 `init_scheduler` 啟動條件，改為「非 TESTING 且
  （非 debug 或 `WERKZEUG_RUN_MAIN=true`）」。
- `tests/test_app_factory.py`（新增）：新增單元測試，驗證 scheduler 啟動條件
  在四種情境下的行為。

### 不會改動的模組

- `app/scheduler.py`（內部邏輯不動，`init_scheduler` 簽章與行為保持不變）。
- `app/scraper.py`、`app/models.py`、`app/routes/*`。
- `docker/Dockerfile`、`docker/docker-compose.yaml`（不切換 web server）。
- `.env`（`FLASK_DEBUG` 開發者可照常使用）。
- 排程間隔（維持 `interval hours=3`）。

## Success Criteria（成功標準）

1. `FLASK_DEBUG=0` 時：`create_app()` 呼叫後 `init_scheduler` 被呼叫且
   BackgroundScheduler 僅啟動一份。
2. `FLASK_DEBUG=1` 時（Werkzeug reloader）：
   - Parent process（環境無 `WERKZEUG_RUN_MAIN`）：`init_scheduler` **不被呼叫**。
   - Child process（`WERKZEUG_RUN_MAIN=true`）：`init_scheduler` 被呼叫。
3. `TESTING=True` 時：`init_scheduler` 永不被呼叫（維持原行為）。
4. 連續啟動服務 10 分鐘以上，`logs/flightprice.log` 不再出現同一排程被兩次
   觸發的紀錄，也不再出現 `uq_flight_scrape_date` 唯一鍵衝突。
5. 新增單元測試全數通過，並覆蓋上述四種情境。

## Risks（風險）

- **風險 1**：若日後改用 gunicorn / uwsgi 等多 worker 部署，單一 process 的
  scheduler 假設會再次失效。此變更不處理多 worker 情境（屬非目標）。
- **風險 2**：`WERKZEUG_RUN_MAIN` 為 Werkzeug 內部約定，Flask/Werkzeug 大版本
  升級時需回歸驗證；目前 Flask 2.x/3.x 與 Werkzeug 2.x/3.x 皆維持此慣例。
- **風險 3**：若開發者以非 `flask run` 的方式啟動（例如直接 `python -m`）
  且未設 debug，行為與 production 相同，屬預期。

## Non-Goals（非目標）

- 不在本變更切換至 gunicorn 或其他多 worker web server。
- 不調整排程間隔（`hours=3` 維持不變）。
- 不新增分散式 lock（例如 Redis-based lock）以支援多實例部署。
- 不重構 `app/scheduler.py` module-level `scheduler` 實例。

## Rollback Strategy（回滾策略）

- 以 `git revert` 回滾本變更的 merge commit 即可復原。
- 由於僅修改 `app/__init__.py` 中單一條件判斷與新增測試檔，回滾不影響資料庫
  結構、docker image 或環境變數。
- 回滾後即回到原本「debug 模式下雙重觸發」狀態，資料層仍有唯一鍵保護不會
  寫入重複資料。
