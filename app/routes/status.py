"""抓取狀態路由。"""

from flask import Blueprint, render_template

status_bp = Blueprint('status', __name__)


@status_bp.route('/status')
def index():
    """顯示抓取狀態頁面。"""
    return render_template('status.html')
