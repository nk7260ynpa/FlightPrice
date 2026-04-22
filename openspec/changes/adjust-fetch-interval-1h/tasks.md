# Tasks: adjust-fetch-interval-1h

## 1. 程式碼調整

- [ ] 1.1 修改 `app/scheduler.py`：將 `scheduler.add_job(..., 'interval', hours=3, ...)` 的 `hours=3` 改為 `hours=1`。
- [ ] 1.2 同步更新 `app/scheduler.py` 的模組 docstring（第 1 行「每 3 小時」→「每 1 小時」）。
- [ ] 1.3 同步更新 `init_scheduler` 的 docstring（「每 3 小時定時抓取任務」→「每 1 小時定時抓取任務」）。
- [ ] 1.4 同步更新 `init_scheduler` 結尾的 `logger.info` 訊息（「每 3 小時」→「每 1 小時」）及 job 註解（第 30 行「# 每 3 小時執行一次」→「# 每 1 小時執行一次」）。
- [ ] 1.5 檔案範圍限制：本組僅允許修改 `app/scheduler.py`，不得修改其他程式碼檔案。

## 2. 測試

- [ ] 2.1 於 `tests/` 新增測試檔 `tests/test_scheduler_interval.py`，涵蓋 `openspec/changes/adjust-fetch-interval-1h/specs/scheduler/spec.md` 中的三個 Scenario：
  - [ ] 2.1.1 Scenario「periodic_scrape job 間隔為 1 小時」：呼叫 `init_scheduler(app)` 後，`scheduler.get_job('periodic_scrape').trigger.interval == datetime.timedelta(hours=1)`。
  - [ ] 2.1.2 Scenario「periodic_scrape job 使用 interval trigger」：`trigger` 為 `apscheduler.triggers.interval.IntervalTrigger` 的實例。
  - [ ] 2.1.3 Scenario「間隔並非 3 小時或其他非預期值」：`trigger.interval` 不等於 `timedelta(hours=3)` 且不等於 `timedelta(minutes=0)`。
- [ ] 2.2 測試中以 `monkeypatch` 將 `apscheduler.schedulers.background.BackgroundScheduler.start` 替換為 no-op，並於 teardown（或 fixture finalizer）呼叫 `app.scheduler.scheduler.remove_all_jobs()`，避免污染其他測試。
- [ ] 2.3 確認 `tests/test_app_factory.py` 既有 5 個 scenarios 全部仍通過（不得修改該檔案內容）。
- [ ] 2.4 於 Docker container 中執行 `pytest tests/ -v`（例如 `docker compose run --rm app pytest tests/ -v` 或 `./run.sh pytest`），全部通過。
- [ ] 2.5 檔案範圍限制：本組僅允許新增 `tests/test_scheduler_interval.py`；不得修改既有測試檔。

## 3. 文件與 spec 同步

- [ ] 3.1 確認 `README.md` 無需修改（目前僅敘述「每日定時從 Skyscanner 擷取」，並未寫出 3 小時週期）。若確有必要再更新，需於 `issues.md` 先記錄並回報 Coordinator。
- [ ] 3.2 檔案範圍限制：本組不得修改 `openspec/specs/scheduler/spec.md`（該檔於 `/opsx:archive` 階段自動由 delta 同步）。
- [ ] 3.3 檔案範圍限制：不得修改 `CLAUDE.md`；如有必要請寫入 `issues.md`。

## 4. 驗收

- [ ] 4.1 `grep -n "hours=3" app/scheduler.py` 應無輸出。
- [ ] 4.2 `grep -n "3 小時" app/scheduler.py` 應無輸出。
- [ ] 4.3 `openspec validate adjust-fetch-interval-1h` 通過。
- [ ] 4.4 所有測試通過；新增測試覆蓋 spec 中全部 3 個 scenario。
