"""價格圖表路由。"""

from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import func

from app import db
from app.models import FlightPrice, TrackedFlight

charts_bp = Blueprint('charts', __name__)


@charts_bp.route('/charts')
def index():
    """顯示價格圖表頁面。"""
    flights = TrackedFlight.query.order_by(TrackedFlight.flight_number).all()
    selected_id = request.args.get('flight_id', type=int)
    return render_template(
        'charts.html', flights=flights, selected_id=selected_id,
    )


@charts_bp.route('/api/charts/<int:flight_id>')
def chart_data(flight_id):
    """取得指定班機的價格歷史資料（JSON）。"""
    flight = TrackedFlight.query.get_or_404(flight_id)

    prices = (
        FlightPrice.query
        .filter_by(flight_number=flight.flight_number)
        .order_by(FlightPrice.scrape_date)
        .all()
    )

    if not prices:
        return jsonify({'labels': [], 'data': [], 'stats': None})

    labels = [p.scrape_date.strftime('%Y-%m-%d') for p in prices]
    data = [float(p.price) for p in prices]

    stats = {
        'max': max(data),
        'min': min(data),
        'avg': round(sum(data) / len(data), 2),
    }

    return jsonify({'labels': labels, 'data': data, 'stats': stats})
