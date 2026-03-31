"""班機管理路由。"""

from datetime import datetime

from flask import (
    Blueprint, flash, jsonify, redirect, render_template, request, url_for,
)

from app import db
from app.flight_lookup import lookup_flight_info
from app.models import TrackedFlight

flights_bp = Blueprint('flights', __name__)


@flights_bp.route('/')
def index():
    """顯示追蹤班機清單頁面。"""
    flights = TrackedFlight.query.order_by(TrackedFlight.created_at.desc()).all()
    return render_template('flights.html', flights=flights)


@flights_bp.route('/api/flights/lookup')
def lookup():
    """查詢航班資訊 API。"""
    flight_number = request.args.get('flight_number', '').strip()
    if not flight_number:
        return jsonify({'error': '請輸入班次代碼'}), 400

    routes = lookup_flight_info(flight_number)
    if routes:
        return jsonify({'routes': routes})

    return jsonify({'error': '無法查詢該班次資訊，請手動輸入'}), 404


@flights_bp.route('/flights/add', methods=['POST'])
def add_flight():
    """新增追蹤班機。"""
    flight_number = request.form.get('flight_number', '').strip()
    departure_date_str = request.form.get('departure_date', '').strip()
    airline = request.form.get('airline', '').strip()
    origin = request.form.get('origin', '').strip()
    destination = request.form.get('destination', '').strip()

    if not flight_number:
        flash('班次代碼為必填欄位', 'error')
        return redirect(url_for('flights.index'))

    if not departure_date_str:
        flash('出發日期為必填欄位', 'error')
        return redirect(url_for('flights.index'))

    try:
        departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('出發日期格式錯誤', 'error')
        return redirect(url_for('flights.index'))

    if not airline or not origin or not destination:
        flash('航空公司、出發地、抵達地皆為必填', 'error')
        return redirect(url_for('flights.index'))

    # 同班次 + 同出發日期視為重複
    existing = TrackedFlight.query.filter_by(
        flight_number=flight_number,
        departure_date=departure_date,
    ).first()
    if existing:
        flash(f'班次 {flight_number}（{departure_date_str}）已在追蹤清單中', 'error')
        return redirect(url_for('flights.index'))

    flight = TrackedFlight(
        flight_number=flight_number,
        airline=airline,
        origin=origin,
        destination=destination,
        departure_date=departure_date,
    )
    db.session.add(flight)
    db.session.commit()

    flash(f'已新增追蹤班機 {flight_number}（{departure_date_str}）', 'success')
    return redirect(url_for('flights.index'))


@flights_bp.route('/flights/<int:flight_id>/toggle', methods=['POST'])
def toggle_flight(flight_id):
    """切換班機追蹤狀態（啟用/停用）。"""
    flight = TrackedFlight.query.get_or_404(flight_id)
    flight.is_active = not flight.is_active
    db.session.commit()

    status = '啟用' if flight.is_active else '停用'
    flash(f'已{status}追蹤 {flight.flight_number}', 'success')
    return redirect(url_for('flights.index'))
