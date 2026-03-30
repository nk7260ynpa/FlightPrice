"""抓取狀態路由。"""

from datetime import date, datetime

from flask import Blueprint, render_template
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
