"""APScheduler 排程設定，每日定時擷取航班價格。"""

import logging

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def init_scheduler(app):
    """初始化排程器，設定每日定時抓取任務。

    Args:
        app: Flask 應用實例。
    """
    def scheduled_scrape():
        with app.app_context():
            from app.scraper import scrape_all_active_flights
            logger.info('開始執行每日定時價格擷取')
            results = scrape_all_active_flights()
            logger.info(
                '每日定時擷取完成: 成功 %d, 失敗 %d',
                results['success'],
                results['failed'],
            )

    # 每日 08:00 執行抓取
    scheduler.add_job(
        scheduled_scrape,
        'cron',
        hour=8,
        minute=0,
        id='daily_scrape',
        replace_existing=True,
    )

    scheduler.start()
    logger.info('排程器已啟動，每日 08:00 執行價格擷取')
