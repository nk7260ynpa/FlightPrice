# Tasks: fix-scheduler-double-trigger

## Task 1: 調整 `create_app()` 中 scheduler 啟動條件

- **檔案範圍**:
  - `app/__init__.py`
- **相依**: 無
- **驗收條件**:
  - [ ] 於 `app/__init__.py` import `os`（已存在，沿用即可）。
  - [ ] 將原本

    ```python
    if not app.config.get('TESTING'):
        from app.scheduler import init_scheduler
        init_scheduler(app)
    ```

    改為：

    ```python
    if not app.config.get('TESTING'):
        if (not app.debug) or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            from app.scheduler import init_scheduler
            init_scheduler(app)
    ```

  - [ ] 不得修改 `app/scheduler.py`、`app/routes/*`、`app/scraper.py`。
  - [ ] 不得修改 `docker/`、`.env`、`requirements.txt`、`run.sh`。
  - [ ] 符合 spec `specs/scheduler/spec.md` 中所有 Scenario 描述的行為。

## Task 2: 新增單元測試覆蓋四種啟動情境

- **檔案範圍**:
  - `tests/test_app_factory.py`（新建）
- **相依**: Task 1
- **驗收條件**:
  - [ ] 新建測試檔 `tests/test_app_factory.py`，使用 `unittest.mock.patch`
    攔截 `app.scheduler.init_scheduler`，驗證其是否被呼叫。
  - [ ] 測試禁止真正啟動 `BackgroundScheduler`（必須 mock，不得在測試中建立
    真實排程 thread）。
  - [ ] 實作測試 `test_testing_mode_does_not_start_scheduler`：
    對應 spec Scenario「測試模式不啟動 scheduler」。
  - [ ] 實作測試 `test_production_mode_starts_scheduler`：
    對應 spec Scenario「Production 模式啟動 scheduler」；以 `monkeypatch.delenv('WERKZEUG_RUN_MAIN', raising=False)`
    與 `test_config={'TESTING': False, 'DEBUG': False}` 設定情境。
  - [ ] 實作測試 `test_debug_reloader_parent_does_not_start_scheduler`：
    對應 spec Scenario「Debug reloader parent 不啟動 scheduler」；
    `app.debug=True` 且 `WERKZEUG_RUN_MAIN` 未設。
  - [ ] 實作測試 `test_debug_reloader_child_starts_scheduler`：
    對應 spec Scenario「Debug reloader child 啟動 scheduler」；
    `app.debug=True` 且 `monkeypatch.setenv('WERKZEUG_RUN_MAIN', 'true')`。
  - [ ] 實作測試 `test_debug_with_werkzeug_run_main_false_does_not_start`：
    對應 spec Scenario「WERKZEUG_RUN_MAIN 為其他值時不啟動」。
  - [ ] 所有測試於 `docker compose run --rm app pytest tests/test_app_factory.py`
    或 `./run.sh pytest tests/test_app_factory.py` 下通過。
  - [ ] 不得修改既有測試檔 `tests/conftest.py`、`tests/test_*.py`。
  - [ ] 不得修改 `app/` 任何檔案（實作已於 Task 1 完成）。

## Task 3: 執行全套測試並確認無回歸

- **檔案範圍**: 無檔案新增／修改
- **相依**: Task 1, Task 2
- **驗收條件**:
  - [ ] 執行 `./run.sh pytest` 或 `docker compose run --rm app pytest`，
    全套測試（含既有 `test_charts.py`、`test_flights.py` 等）通過。
  - [ ] 若任一既有測試失敗，於 `issues.md` 記錄並回報 Coordinator，不得
    自行修改超出範圍的檔案。

---

## 超出範圍時的處理

若 Specialist 實作中發現需要修改以下檔案，**不得自行修改**，須於
`openspec/changes/fix-scheduler-double-trigger/issues.md` 記錄後回報
Coordinator：

- `README.md`、`CLAUDE.md`
- `docker/Dockerfile`、`docker/docker-compose.yaml`、`run.sh`
- `app/scheduler.py`（本次不動 scheduler 內部邏輯）
- `.env`、`requirements.txt`
- 其他未於 Task 1／Task 2 宣告的檔案
