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
