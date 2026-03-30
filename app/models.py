"""SQLAlchemy 資料模型定義。"""

from datetime import datetime

from app import db


class TrackedFlight(db.Model):
    """追蹤班機清單資料表。"""

    __tablename__ = 'tracked_flights'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_number = db.Column(db.String(20), nullable=False)
    airline = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # 同班次 + 同出發日期唯一
    __table_args__ = (
        db.UniqueConstraint('flight_number', 'departure_date', name='uq_flight_date'),
    )

    prices = db.relationship('FlightPrice', backref='tracked_flight', lazy=True)

    def __repr__(self):
        return f'<TrackedFlight {self.flight_number} {self.departure_date}>'


class FlightPrice(db.Model):
    """航班價格紀錄資料表。"""

    __tablename__ = 'flight_prices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_number = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    scrape_date = db.Column(db.Date, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=True)
    airline = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    tracked_flight_id = db.Column(
        db.Integer, db.ForeignKey('tracked_flights.id'), nullable=True
    )

    def __repr__(self):
        return f'<FlightPrice {self.flight_number} {self.price} {self.scrape_date}>'


class ScrapeLog(db.Model):
    """抓取狀態紀錄資料表。"""

    __tablename__ = 'scrape_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 'success' 或 'failed'
    error_message = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    scraped_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f'<ScrapeLog {self.flight_number} {self.status} {self.scraped_at}>'
