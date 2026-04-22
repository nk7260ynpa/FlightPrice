# Design: fix-scheduler-double-trigger

## Architecture Decision

### 選定方案：B — 以 `WERKZEUG_RUN_MAIN` 判斷 reloader child

在 `app/__init__.py` 的 `create_app()` 中，將原本

```python
if not app.config.get('TESTING'):
    init_scheduler(app)
```

改為

```python
if not app.config.get('TESTING'):
    if (not app.debug) or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        init_scheduler(app)
```

- Werkzeug auto-reloader 啟動 child process 前會設 `WERKZEUG_RUN_MAIN=true`；
  parent（watchdog 用）process 則不會。
- `app.debug` 由 Flask 依 `FLASK_DEBUG` 環境變數決定。

### 被否決的替代方案

#### 方案 A：關閉 debug 模式

- 做法：強制 `FLASK_DEBUG=0`，或在 `create_app()` 內呼叫 `init_scheduler` 前
  檢查並拒絕 debug。
- 否決理由：犧牲開發者體驗（失去 auto-reload 與 debugger），治標不治本。
  debug 模式本身沒有錯，錯的是我們在兩個 process 都啟動 scheduler。

#### 方案 C：換 gunicorn / 改為外部排程器

- 做法：改用 gunicorn 單 worker 啟動 Flask，或將排程移出 Flask process
  （例如獨立的 `scheduler_worker` container、或改用 cron / Celery beat）。
- 否決理由：變更範圍過大，涉及 `docker/Dockerfile`、`docker-compose.yaml`、
  `run.sh`、甚至排程器選型。本次僅需修正 bug，該重構留給後續 proposal。

### 選 B 的理由

1. **最小侵入**：只改一個條件判斷，不影響開發者體驗，不改 docker/部署腳本。
2. **與 Flask 官方 debug 模式相容**：`WERKZEUG_RUN_MAIN` 是 Werkzeug 公開的
   reloader 約定（Flask 文件中的 `flask.cli.ScriptInfo` 與 reloader 章節皆
   使用此變數），語意穩定。
3. **可測試**：條件全部由 `app.config`、`app.debug` 與 `os.environ` 組成，
   以 `monkeypatch` 即可覆蓋所有情境。

## Component Design

### 受影響元件

```
create_app()  ──(判斷啟動條件)──►  init_scheduler(app)
    ▲                                       │
    │                                       ▼
os.environ['WERKZEUG_RUN_MAIN']      BackgroundScheduler.start()
app.debug
app.config['TESTING']
```

### 啟動條件真值表

| 情境 | TESTING | app.debug | WERKZEUG_RUN_MAIN | 呼叫 init_scheduler |
| --- | --- | --- | --- | --- |
| 測試 | True | any | any | 否 |
| Production / 非 debug | False | False | 未設 | **是** |
| Debug reloader parent | False | True | 未設 | 否 |
| Debug reloader child | False | True | `'true'` | **是** |
| Debug 但未 fork（少見） | False | True | 未設 | 否（保守，避免誤啟動）|

註：最後一列為保守策略；若未來有需求可再放寬，但目前以「debug 一律要求
child flag」作為簡潔判斷。

### 介面定義

- `create_app()` 簽章不變。
- `init_scheduler(app)` 簽章與實作不變。
- 不新增公開 API。

## Dependencies

### 外部套件

- `Flask`（已存在於 `requirements.txt`）
- `APScheduler`（已存在，不升版）
- `python-dotenv`（已存在）
- 測試：`pytest`、`pytest` 內建 `monkeypatch`（已存在，無新增）

### 內部模組相依

- `app/__init__.py` 依賴 `os` 標準函式庫（已 import）。
- 測試檔依賴 `app.create_app` 與 `unittest.mock.patch`。

## Migration

- **資料遷移**：無。
- **環境變數**：無新增；`WERKZEUG_RUN_MAIN` 由 Werkzeug 自動設定，開發者
  無須手動配置。
- **向下相容**：對既有 production 部署（`FLASK_DEBUG=0`）行為完全一致；
  對 debug 開發者而言，scheduler 改由 reloader child 啟動，行為仍相同，
  僅消除重複觸發。
