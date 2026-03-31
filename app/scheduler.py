"""APScheduler 排程設定，每 3 小時檢查並擷取航班價格。"""

import logging

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def init_scheduler(app):
    """初始化排程器，設定每 3 小時定時抓取任務。

    Args:
        app: Flask 應用實例。
    """
    def scheduled_scrape():
        with app.app_context():
            from app.scraper import scrape_all_active_flights
            logger.info('開始執行定時價格擷取檢查')
            results = scrape_all_active_flights()
            logger.info(
                '定時擷取完成: 成功 %d, 失敗 %d, 跳過 %d',
                results['success'],
                results['failed'],
                results['skipped'],
            )

    # 每 3 小時執行一次
    scheduler.add_job(
        scheduled_scrape,
        'interval',
        hours=3,
        id='periodic_scrape',
        replace_existing=True,
    )

    scheduler.start()
    logger.info('排程器已啟動，每 3 小時執行價格擷取檢查')
