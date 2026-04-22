"""測試 `create_app()` 中排程器啟動條件。

對應 spec `openspec/changes/fix-scheduler-double-trigger/specs/scheduler/spec.md`
中的五個 Scenario，驗證在不同 `TESTING` / `app.debug` / `WERKZEUG_RUN_MAIN`
組合下，`init_scheduler` 是否被呼叫。

本測試以 `unittest.mock.patch` 攔截 `app.scheduler.init_scheduler`，避免
真正啟動 `BackgroundScheduler` thread，確保測試可重複執行且無副作用。
"""

from unittest.mock import patch

import pytest

from app import create_app


@pytest.fixture
def sqlite_config():
    """提供測試可用的 SQLite in-memory 設定基底。

    Returns:
        dict: Flask 設定字典，呼叫端可再覆蓋 `TESTING`、`DEBUG` 等欄位。
    """
    return {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    }


def test_testing_mode_does_not_start_scheduler(monkeypatch, sqlite_config):
    """測試模式不啟動 scheduler。

    對應 Scenario「測試模式不啟動 scheduler」：
    當 `TESTING=True` 時，無論其他環境變數為何，`init_scheduler` 皆不應被呼叫。
    """
    monkeypatch.setenv('WERKZEUG_RUN_MAIN', 'true')  # 即使設定也不應啟動
    config = {**sqlite_config, 'TESTING': True}

    with patch('app.scheduler.init_scheduler') as mock_init:
        create_app(test_config=config)

    mock_init.assert_not_called()


def test_production_mode_starts_scheduler(monkeypatch, sqlite_config):
    """Production 模式啟動 scheduler。

    對應 Scenario「Production 模式啟動 scheduler」：
    `TESTING=False`、`app.debug=False`、`WERKZEUG_RUN_MAIN` 未設，
    `init_scheduler(app)` 應被呼叫恰好 1 次。
    """
    monkeypatch.delenv('WERKZEUG_RUN_MAIN', raising=False)
    config = {**sqlite_config, 'TESTING': False, 'DEBUG': False}

    with patch('app.scheduler.init_scheduler') as mock_init:
        create_app(test_config=config)

    assert mock_init.call_count == 1


def test_debug_reloader_parent_does_not_start_scheduler(
        monkeypatch, sqlite_config):
    """Debug reloader parent 不啟動 scheduler。

    對應 Scenario「Debug reloader parent 不啟動 scheduler」：
    `app.debug=True` 且 `WERKZEUG_RUN_MAIN` 未設，`init_scheduler` 不應被呼叫。
    """
    monkeypatch.delenv('WERKZEUG_RUN_MAIN', raising=False)
    config = {**sqlite_config, 'TESTING': False, 'DEBUG': True}

    with patch('app.scheduler.init_scheduler') as mock_init:
        create_app(test_config=config)

    mock_init.assert_not_called()


def test_debug_reloader_child_starts_scheduler(monkeypatch, sqlite_config):
    """Debug reloader child 啟動 scheduler。

    對應 Scenario「Debug reloader child 啟動 scheduler」：
    `app.debug=True` 且 `WERKZEUG_RUN_MAIN='true'`，`init_scheduler(app)`
    應被呼叫恰好 1 次。
    """
    monkeypatch.setenv('WERKZEUG_RUN_MAIN', 'true')
    config = {**sqlite_config, 'TESTING': False, 'DEBUG': True}

    with patch('app.scheduler.init_scheduler') as mock_init:
        create_app(test_config=config)

    assert mock_init.call_count == 1


def test_debug_with_werkzeug_run_main_false_does_not_start(
        monkeypatch, sqlite_config):
    """WERKZEUG_RUN_MAIN 為非 'true' 字串時不啟動（debug 情境）。

    對應 Scenario「WERKZEUG_RUN_MAIN 為其他值時不啟動」：
    `app.debug=True` 且 `WERKZEUG_RUN_MAIN='false'`，`init_scheduler` 不應被呼叫。
    """
    monkeypatch.setenv('WERKZEUG_RUN_MAIN', 'false')
    config = {**sqlite_config, 'TESTING': False, 'DEBUG': True}

    with patch('app.scheduler.init_scheduler') as mock_init:
        create_app(test_config=config)

    mock_init.assert_not_called()
