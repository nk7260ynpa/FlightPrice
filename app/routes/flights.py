"""班機管理路由。"""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models import TrackedFlight

flights_bp = Blueprint('flights', __name__)


@flights_bp.route('/')
def index():
    """顯示追蹤班機清單頁面。"""
    flights = TrackedFlight.query.order_by(TrackedFlight.created_at.desc()).all()
    return render_template('flights.html', flights=flights)


@flights_bp.route('/flights/add', methods=['POST'])
def add_flight():
    """新增追蹤班機。"""
    flight_number = request.form.get('flight_number', '').strip()
    airline = request.form.get('airline', '').strip()
    origin = request.form.get('origin', '').strip()
    destination = request.form.get('destination', '').strip()

    if not flight_number:
        flash('班次編號為必填欄位', 'error')
        return redirect(url_for('flights.index'))

    if not airline or not origin or not destination:
        flash('所有欄位皆為必填', 'error')
        return redirect(url_for('flights.index'))

    existing = TrackedFlight.query.filter_by(
        flight_number=flight_number
    ).first()
    if existing:
        flash('該班次已在追蹤清單中', 'error')
        return redirect(url_for('flights.index'))

    flight = TrackedFlight(
        flight_number=flight_number,
        airline=airline,
        origin=origin,
        destination=destination,
    )
    db.session.add(flight)
    db.session.commit()

    flash(f'已新增追蹤班機 {flight_number}', 'success')
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
