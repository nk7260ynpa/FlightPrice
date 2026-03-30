"""測試共用 fixtures。"""

import pytest

from app import create_app, db as _db


@pytest.fixture
def app():
    """建立測試用 Flask 應用（使用 SQLite in-memory）。"""
    test_app = create_app(test_config={
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
    })

    with test_app.app_context():
        _db.create_all()
        yield test_app
        _db.drop_all()


@pytest.fixture
def client(app):
    """建立測試用 HTTP 客戶端。"""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """建立測試用資料庫 session。"""
    with app.app_context():
        yield _db.session
