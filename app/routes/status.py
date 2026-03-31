"""抓取狀態路由。"""

from datetime import date, datetime

from flask import Blueprint, flash, redirect, render_template, url_for
from sqlalchemy import func

from app.models import ScrapeLog, TrackedFlight

status_bp = Blueprint('status', __name__)


@status_bp.route('/status')
def index():
    """顯示今日抓取狀態頁面。"""
    today = date.today()

    # 查詢今日所有抓取紀錄
    logs = (
        ScrapeLog.query
        .filter(func.date(ScrapeLog.scraped_at) == today)
        .order_by(ScrapeLog.scraped_at.desc())
        .all()
    )

    # 統計
    total_tracked = TrackedFlight.query.filter_by(is_active=True).count()
    success_count = sum(1 for log in logs if log.status == 'success')
    failed_count = sum(1 for log in logs if log.status == 'failed')

    return render_template(
        'status.html',
        logs=logs,
        total_tracked=total_tracked,
        success_count=success_count,
        failed_count=failed_count,
        has_logs=len(logs) > 0,
    )


@status_bp.route('/status/scrape', methods=['POST'])
def force_scrape():
    """強制執行價格抓取。"""
    from app.scraper import force_scrape_all_active_flights

    results = force_scrape_all_active_flights()

    if results['total'] == 0:
        flash('無啟用班機可抓取', 'warning')
    else:
        flash(
            f'強制抓取完成：成功 {results["success"]}，失敗 {results["failed"]}',
            'success' if results['failed'] == 0 else 'warning',
        )

    return redirect(url_for('status.index'))
