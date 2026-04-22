# scheduler Specification

## Purpose

定義 FlightPrice 應用程式啟動時，背景排程器（`BackgroundScheduler`）的啟動條件，確保 `init_scheduler(app)` 不會在 Flask debug 模式下因 Werkzeug auto-reloader 而重複啟動。

## Requirements

### Requirement: Debug 模式下 Scheduler 僅於 Reloader Child Process 啟動

The system SHALL ensure that `init_scheduler(app)` is invoked **at most once**
per `create_app()` call, and only in the process that actually serves
requests, regardless of whether Flask runs in debug mode with the Werkzeug
auto-reloader.

具體啟動條件為：

> `app.config['TESTING']` 為 False **且**
> （`app.debug` 為 False **或** `os.environ['WERKZEUG_RUN_MAIN'] == 'true'`）。

#### Scenario: 測試模式不啟動 scheduler

- **GIVEN** `create_app()` 以 `test_config={'TESTING': True}` 呼叫
- **WHEN** `create_app()` 執行完畢
- **THEN** `init_scheduler` 不被呼叫，無 `BackgroundScheduler` 被建立或啟動

#### Scenario: Production 模式啟動 scheduler

- **GIVEN** `app.config['TESTING']` 為 False
- **AND** `app.debug` 為 False
- **AND** 環境變數 `WERKZEUG_RUN_MAIN` 未設定
- **WHEN** `create_app()` 執行完畢
- **THEN** `init_scheduler(app)` 被呼叫恰好 1 次

#### Scenario: Debug reloader parent 不啟動 scheduler

- **GIVEN** `app.config['TESTING']` 為 False
- **AND** `app.debug` 為 True
- **AND** 環境變數 `WERKZEUG_RUN_MAIN` 未設定
- **WHEN** `create_app()` 執行完畢
- **THEN** `init_scheduler` 不被呼叫

#### Scenario: Debug reloader child 啟動 scheduler

- **GIVEN** `app.config['TESTING']` 為 False
- **AND** `app.debug` 為 True
- **AND** 環境變數 `WERKZEUG_RUN_MAIN` 設為字串 `'true'`
- **WHEN** `create_app()` 執行完畢
- **THEN** `init_scheduler(app)` 被呼叫恰好 1 次

#### Scenario: WERKZEUG_RUN_MAIN 為其他值時不啟動（debug 情境）

- **GIVEN** `app.config['TESTING']` 為 False
- **AND** `app.debug` 為 True
- **AND** 環境變數 `WERKZEUG_RUN_MAIN` 設為 `'false'` 或其他非 `'true'` 字串
- **WHEN** `create_app()` 執行完畢
- **THEN** `init_scheduler` 不被呼叫

### Requirement: 定時抓取週期為 1 小時

The system SHALL register the periodic flight-price scrape job with an
`interval` trigger whose period equals **exactly 1 hour**
(`timedelta(hours=1)`), so that `scrape_all_active_flights()` is invoked once
per hour while the scheduler is running.

具體規範：

> 於 `init_scheduler(app)` 中呼叫 `scheduler.add_job(...)` 所建立的
> `id='periodic_scrape'` job 必須使用 `trigger='interval'` 且
> `trigger.interval == timedelta(hours=1)`。

#### Scenario: periodic_scrape job 間隔為 1 小時

- **GIVEN** 一個以 `test_config={'TESTING': False}` 建立的 Flask app
- **AND** `BackgroundScheduler.start` 已被 patch 為 no-op 以避免副作用
- **WHEN** 呼叫 `init_scheduler(app)`
- **THEN** `scheduler.get_job('periodic_scrape')` 不為 `None`
- **AND** 該 job 的 `trigger.interval` 等於 `datetime.timedelta(hours=1)`

#### Scenario: periodic_scrape job 使用 interval trigger

- **GIVEN** 同上前置條件
- **WHEN** 呼叫 `init_scheduler(app)` 完成
- **THEN** `scheduler.get_job('periodic_scrape').trigger` 為
  `apscheduler.triggers.interval.IntervalTrigger` 的實例

#### Scenario: 間隔並非 3 小時或其他非預期值

- **GIVEN** 同上前置條件
- **WHEN** 呼叫 `init_scheduler(app)` 完成
- **THEN** `scheduler.get_job('periodic_scrape').trigger.interval` **不等於**
  `datetime.timedelta(hours=3)`
- **AND** 也不等於 `datetime.timedelta(minutes=0)`
