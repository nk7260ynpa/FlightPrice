"""價格圖表路由。"""

from flask import Blueprint, render_template

charts_bp = Blueprint('charts', __name__)


@charts_bp.route('/charts')
def index():
    """顯示價格圖表頁面。"""
    return render_template('charts.html')
