"""資料庫初始化腳本。

容器啟動時執行以確保資料表存在。
"""

import logging

from app import create_app, db

logger = logging.getLogger(__name__)


def init_database():
    """建立所有資料表。"""
    app = create_app()
    with app.app_context():
        db.create_all()
        logger.info('資料庫初始化完成，所有資料表已建立')


if __name__ == '__main__':
    init_database()
