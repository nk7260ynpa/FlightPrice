"""爬蟲模組單元測試。"""

from unittest.mock import patch, MagicMock
from datetime import date

from app import db
from app.models import FlightPrice, ScrapeLog, TrackedFlight
from app.scraper import (
    force_scrape_all_active_flights,
    scrape_all_active_flights,
    scrape_flight_price,
)


class TestScrapeFlightPrice:
    """scrape_flight_price 函式測試。"""

    def _create_tracked_flight(self, db_session):
        """建立測試用追蹤班機。"""
        flight = TrackedFlight(
            flight_number='CI-100',
            airline='中華航空',
            origin='TPE',
            destination='NRT',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()
        return flight

    @patch('app.scraper._fetch_price_from_skyscanner')
    def test_scrape_success(self, mock_fetch, app, db_session):
        """測試成功擷取價格。"""
        flight = self._create_tracked_flight(db_session)
        mock_fetch.return_value = {
            'price': 12500.00,
            'departure_time': None,
        }

        with patch.dict('os.environ', {'SKYSCANNER_API_KEY': 'test-key'}):
            result = scrape_flight_price(flight)

        assert result is not None
        assert float(result.price) == 12500.00

        price_record = FlightPrice.query.filter_by(
            flight_number='CI-100'
        ).first()
        assert price_record is not None

        log = ScrapeLog.query.filter_by(flight_number='CI-100').first()
        assert log.status == 'success'

    def test_scrape_no_api_key(self, app, db_session):
        """測試未設定 API key 時記錄失敗。"""
        flight = self._create_tracked_flight(db_session)

        with patch.dict('os.environ', {'SKYSCANNER_API_KEY': ''}):
            result = scrape_flight_price(flight)

        assert result is None
        log = ScrapeLog.query.filter_by(flight_number='CI-100').first()
        assert log.status == 'failed'
        assert 'SKYSCANNER_API_KEY' in log.error_message

    @patch('app.scraper._fetch_price_from_skyscanner')
    def test_scrape_api_returns_none(self, mock_fetch, app, db_session):
        """測試 API 未找到價格資料。"""
        flight = self._create_tracked_flight(db_session)
        mock_fetch.return_value = None

        with patch.dict('os.environ', {'SKYSCANNER_API_KEY': 'test-key'}):
            result = scrape_flight_price(flight)

        assert result is None
        log = ScrapeLog.query.filter_by(flight_number='CI-100').first()
        assert log.status == 'failed'

    @patch('app.scraper._fetch_price_from_skyscanner')
    def test_scrape_api_exception(self, mock_fetch, app, db_session):
        """測試 API 拋出例外時記錄失敗。"""
        flight = self._create_tracked_flight(db_session)
        mock_fetch.side_effect = Exception('連線逾時')

        with patch.dict('os.environ', {'SKYSCANNER_API_KEY': 'test-key'}):
            result = scrape_flight_price(flight)

        assert result is None
        log = ScrapeLog.query.filter_by(flight_number='CI-100').first()
        assert log.status == 'failed'
        assert '連線逾時' in log.error_message


class TestScrapeAllActiveFlights:
    """scrape_all_active_flights 函式測試。"""

    @patch('app.scraper._fetch_price_from_skyscanner')
    def test_scrape_only_active_flights(self, mock_fetch, app, db_session):
        """測試只擷取啟用的班機。"""
        active = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT', is_active=True,
            departure_date=date(2026, 5, 1),
        )
        inactive = TrackedFlight(
            flight_number='BR-001', airline='長榮航空',
            origin='TPE', destination='LAX', is_active=False,
            departure_date=date(2026, 5, 1),
        )
        db_session.add_all([active, inactive])
        db_session.commit()

        mock_fetch.return_value = {'price': 10000.00, 'departure_time': None}

        with patch.dict('os.environ', {'SKYSCANNER_API_KEY': 'test-key'}):
            results = scrape_all_active_flights()

        assert results['total'] == 1
        assert results['success'] == 1

        # 確認只有 CI-100 有價格紀錄
        prices = FlightPrice.query.all()
        assert len(prices) == 1
        assert prices[0].flight_number == 'CI-100'

    def test_scrape_no_active_flights(self, app, db_session):
        """測試無啟用班機時的結果。"""
        results = scrape_all_active_flights()
        assert results['total'] == 0
        assert results['success'] == 0
        assert results['failed'] == 0
        assert results['skipped'] == 0

    @patch('app.scraper._fetch_price_from_skyscanner')
    def test_skip_flight_with_today_data(self, mock_fetch, app, db_session):
        """測試當日已有資料的班機被跳過。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT', is_active=True,
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        # 建立當日已有的價格資料
        existing_price = FlightPrice(
            flight_number='CI-100', price=12000,
            scrape_date=date.today(), airline='中華航空',
            origin='TPE', destination='NRT',
        )
        db_session.add(existing_price)
        db_session.commit()

        results = scrape_all_active_flights()

        assert results['total'] == 1
        assert results['skipped'] == 1
        assert results['success'] == 0
        mock_fetch.assert_not_called()

    @patch('app.scraper._fetch_price_from_skyscanner')
    def test_scrape_flight_without_today_data(self, mock_fetch, app, db_session):
        """測試當日無資料的班機正常擷取。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT', is_active=True,
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        mock_fetch.return_value = {'price': 12000, 'departure_time': None}

        with patch.dict('os.environ', {'SKYSCANNER_API_KEY': 'test-key'}):
            results = scrape_all_active_flights()

        assert results['total'] == 1
        assert results['success'] == 1
        assert results['skipped'] == 0


class TestForceScrapeAllActiveFlights:
    """force_scrape_all_active_flights 函式測試。"""

    @patch('app.scraper._fetch_price_from_skyscanner')
    def test_force_scrape_ignores_existing_data(self, mock_fetch, app, db_session):
        """測試強制抓取不跳過當日已有資料的班機。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT', is_active=True,
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        existing_price = FlightPrice(
            flight_number='CI-100', price=12000,
            scrape_date=date.today(), airline='中華航空',
            origin='TPE', destination='NRT',
        )
        db_session.add(existing_price)
        db_session.commit()

        mock_fetch.return_value = {'price': 11500, 'departure_time': None}

        with patch.dict('os.environ', {'SKYSCANNER_API_KEY': 'test-key'}):
            results = force_scrape_all_active_flights()

        assert results['total'] == 1
        assert results['success'] == 1
        mock_fetch.assert_called_once()

    def test_force_scrape_no_active_flights(self, app, db_session):
        """測試無啟用班機時的結果。"""
        results = force_scrape_all_active_flights()
        assert results['total'] == 0
        assert results['success'] == 0
