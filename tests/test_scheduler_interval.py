"""測試 `init_scheduler` 註冊的 periodic_scrape job 間隔設定。

對應 spec `openspec/changes/adjust-fetch-interval-1h/specs/scheduler/spec.md`
中的三個 Scenario，驗證：

1. `trigger.interval` 等於 `timedelta(hours=1)`。
2. `trigger` 為 `IntervalTrigger` 的實例。
3. `trigger.interval` 不等於 `timedelta(hours=3)` 亦不等於 `timedelta(minutes=0)`。

為避免真正啟動 `BackgroundScheduler` 背景 thread，本檔以 `monkeypatch`
將 `BackgroundScheduler.start` 替換為 no-op；並於 fixture finalizer
呼叫 `scheduler.remove_all_jobs()` 清理，避免污染其他測試。
"""

from datetime import timedelta

import pytest
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app import create_app
from app import scheduler as scheduler_module


@pytest.fixture
def initialized_scheduler(monkeypatch):
    """初始化 scheduler 並回傳其 periodic_scrape job。

    Steps:
        1. Patch `BackgroundScheduler.start` 為 no-op，避免啟動背景 thread。
        2. 建立 `TESTING=False` 的 Flask app（此 config 讓 `init_scheduler`
           可以安全被呼叫，但我們這裡直接呼叫 `init_scheduler(app)`
           以隔離 `create_app` 的啟動條件判斷）。
        3. 呼叫 `init_scheduler(app)`。
        4. yield 給測試；teardown 時清空已註冊 job 避免污染其他測試。
    """
    monkeypatch.setattr(BackgroundScheduler, 'start', lambda self, *a, **kw: None)

    app = create_app(test_config={
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
    })
    scheduler_module.init_scheduler(app)
    try:
        yield scheduler_module.scheduler
    finally:
        scheduler_module.scheduler.remove_all_jobs()


def test_periodic_scrape_interval_is_one_hour(initialized_scheduler):
    """Scenario「periodic_scrape job 間隔為 1 小時」。

    呼叫 `init_scheduler(app)` 後，`periodic_scrape` job 存在且
    `trigger.interval` 等於 `timedelta(hours=1)`。
    """
    job = initialized_scheduler.get_job('periodic_scrape')
    assert job is not None
    assert job.trigger.interval == timedelta(hours=1)


def test_periodic_scrape_uses_interval_trigger(initialized_scheduler):
    """Scenario「periodic_scrape job 使用 interval trigger」。

    `periodic_scrape` 的 `trigger` 必須為 `IntervalTrigger` 的實例。
    """
    job = initialized_scheduler.get_job('periodic_scrape')
    assert isinstance(job.trigger, IntervalTrigger)


def test_periodic_scrape_interval_is_not_unexpected_value(initialized_scheduler):
    """Scenario「間隔並非 3 小時或其他非預期值」。

    `trigger.interval` 不等於 `timedelta(hours=3)` 且不等於
    `timedelta(minutes=0)`，避免誤改回舊值或意外清空。
    """
    job = initialized_scheduler.get_job('periodic_scrape')
    assert job.trigger.interval != timedelta(hours=3)
    assert job.trigger.interval != timedelta(minutes=0)
