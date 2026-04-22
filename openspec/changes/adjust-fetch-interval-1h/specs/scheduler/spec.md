# scheduler Delta for adjust-fetch-interval-1h

## ADDED Requirements

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
