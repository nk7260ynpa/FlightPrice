"""資料模型單元測試。"""

from datetime import date, datetime

from app import db
from app.models import FlightPrice, ScrapeLog, TrackedFlight


class TestTrackedFlight:
    """TrackedFlight 資料模型測試。"""

    def test_create_tracked_flight(self, app, db_session):
        """測試新增追蹤班機。"""
        flight = TrackedFlight(
            flight_number='CI-100',
            airline='中華航空',
            origin='TPE',
            destination='NRT',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        result = TrackedFlight.query.filter_by(flight_number='CI-100').first()
        assert result is not None
        assert result.airline == '中華航空'
        assert result.departure_date == date(2026, 5, 1)
        assert result.is_active is True

    def test_unique_flight_and_date(self, app, db_session):
        """測試同班次同出發日期的唯一性約束。"""
        flight1 = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight1)
        db_session.commit()

        flight2 = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight2)
        import sqlalchemy
        try:
            db_session.commit()
            assert False, '應拋出唯一性約束錯誤'
        except sqlalchemy.exc.IntegrityError:
            db_session.rollback()

    def test_same_flight_different_date(self, app, db_session):
        """測試同班次不同出發日期可同時存在。"""
        for d in [date(2026, 5, 1), date(2026, 5, 15)]:
            flight = TrackedFlight(
                flight_number='CI-100', airline='中華航空',
                origin='TPE', destination='NRT',
                departure_date=d,
            )
            db_session.add(flight)
        db_session.commit()

        results = TrackedFlight.query.filter_by(flight_number='CI-100').all()
        assert len(results) == 2

    def test_deactivate_flight(self, app, db_session):
        """測試停用追蹤班機。"""
        flight = TrackedFlight(
            flight_number='BR-001', airline='長榮航空',
            origin='TPE', destination='LAX',
            departure_date=date(2026, 6, 1),
        )
        db_session.add(flight)
        db_session.commit()

        flight.is_active = False
        db_session.commit()

        result = TrackedFlight.query.filter_by(flight_number='BR-001').first()
        assert result.is_active is False


class TestFlightPrice:
    """FlightPrice 資料模型測試。"""

    def test_create_flight_price(self, app, db_session):
        """測試新增航班價格紀錄。"""
        price = FlightPrice(
            flight_number='CI-100',
            price=12500.00,
            scrape_date=date(2026, 3, 30),
            departure_time=datetime(2026, 5, 1, 8, 30),
            airline='中華航空',
            origin='TPE',
            destination='NRT',
        )
        db_session.add(price)
        db_session.commit()

        result = FlightPrice.query.filter_by(flight_number='CI-100').first()
        assert result is not None
        assert float(result.price) == 12500.00

    def test_multiple_prices_same_flight_same_day(self, app, db_session):
        """測試同一班次同一天可有多筆紀錄。"""
        for price_val in [12500.00, 12800.00]:
            price = FlightPrice(
                flight_number='CI-100',
                price=price_val,
                scrape_date=date(2026, 3, 30),
                airline='中華航空',
                origin='TPE',
                destination='NRT',
            )
            db_session.add(price)
        db_session.commit()

        results = FlightPrice.query.filter_by(
            flight_number='CI-100',
            scrape_date=date(2026, 3, 30),
        ).all()
        assert len(results) == 2


class TestScrapeLog:
    """ScrapeLog 資料模型測試。"""

    def test_create_success_log(self, app, db_session):
        """測試記錄成功抓取。"""
        log = ScrapeLog(
            flight_number='CI-100',
            status='success',
            price=12500.00,
        )
        db_session.add(log)
        db_session.commit()

        result = ScrapeLog.query.filter_by(flight_number='CI-100').first()
        assert result.status == 'success'
        assert result.error_message is None

    def test_create_failed_log(self, app, db_session):
        """測試記錄失敗抓取。"""
        log = ScrapeLog(
            flight_number='CI-100',
            status='failed',
            error_message='連線逾時',
        )
        db_session.add(log)
        db_session.commit()

        result = ScrapeLog.query.filter_by(flight_number='CI-100').first()
        assert result.status == 'failed'
        assert result.error_message == '連線逾時'
