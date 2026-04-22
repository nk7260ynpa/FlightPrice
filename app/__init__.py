"""FlightPrice Flask 應用工廠。"""

import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def create_app(test_config=None):
    """建立並設定 Flask 應用。

    Args:
        test_config: 測試用設定字典，提供時會覆蓋預設設定。
    """
    app = Flask(__name__)

    # 資料庫設定
    mysql_user = os.getenv('MYSQL_USER', 'flightprice')
    mysql_password = os.getenv('MYSQL_PASSWORD', 'password')
    mysql_host = os.getenv('MYSQL_HOST', 'db')
    mysql_port = os.getenv('MYSQL_PORT', '3306')
    mysql_database = os.getenv('MYSQL_DATABASE', 'flightprice')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'mysql+pymysql://{mysql_user}:{mysql_password}'
        f'@{mysql_host}:{mysql_port}/{mysql_database}'
    )

    if test_config:
        app.config.update(test_config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

    db.init_app(app)

    # 註冊路由藍圖
    from app.routes.flights import flights_bp
    from app.routes.charts import charts_bp
    from app.routes.status import status_bp

    app.register_blueprint(flights_bp)
    app.register_blueprint(charts_bp)
    app.register_blueprint(status_bp)

    # 建立資料表
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    # 設定 logging
    _setup_logging(app)

    # 啟動排程器（測試模式下不啟動；debug 模式下僅於 Werkzeug reloader child 啟動）
    if not app.config.get('TESTING'):
        if (not app.debug) or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            from app.scheduler import init_scheduler
            init_scheduler(app)

    return app


def _setup_logging(app):
    """設定日誌輸出至 logs 資料夾。"""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'flightprice.log'),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s: %(message)s'
    ))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
