"""爬蟲模組單元測試。"""

from unittest.mock import patch, MagicMock
from datetime import date

from app import db
from app.models import FlightPrice, ScrapeLog, TrackedFlight
from app.scraper import (
    _fetch_price_via_playwright,
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

    @patch('app.scraper._fetch_price_via_playwright')
    def test_scrape_no_api_key_uses_playwright(self, mock_pw, app, db_session):
        """測試未設定 API Key 時使用 Playwright。"""
        flight = self._create_tracked_flight(db_session)
        mock_pw.return_value = {'price': 11000, 'departure_time': None}

        with patch.dict('os.environ', {'SKYSCANNER_API_KEY': ''}):
            result = scrape_flight_price(flight)

        assert result is not None
        assert float(result.price) == 11000.0
        mock_pw.assert_called_once()

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

    @patch('app.scraper._fetch_price_from_skyscanner')
    def test_scrape_skip_when_today_data_exists(self, mock_fetch, app, db_session):
        """測試當日已有資料時跳過擷取。"""
        flight = self._create_tracked_flight(db_session)

        existing_price = FlightPrice(
            flight_number='CI-100', price=12000,
            scrape_date=date.today(), airline='中華航空',
            origin='TPE', destination='NRT',
        )
        db_session.add(existing_price)
        db_session.commit()

        with patch.dict('os.environ', {'SKYSCANNER_API_KEY': 'test-key'}):
            result = scrape_flight_price(flight)

        assert result is None
        mock_fetch.assert_not_called()


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


class TestFlightPriceUniqueConstraint:
    """FlightPrice 唯一約束測試。"""

    def test_duplicate_flight_scrape_date_rejected(self, app, db_session):
        """測試同一班機同一天重複寫入被拒絕。"""
        from sqlalchemy.exc import IntegrityError

        price1 = FlightPrice(
            flight_number='CI-100', price=12000,
            scrape_date=date.today(), airline='中華航空',
            origin='TPE', destination='NRT',
        )
        db_session.add(price1)
        db_session.commit()

        price2 = FlightPrice(
            flight_number='CI-100', price=11500,
            scrape_date=date.today(), airline='中華航空',
            origin='TPE', destination='NRT',
        )
        db_session.add(price2)

        try:
            db_session.commit()
            assert False, '應拋出 IntegrityError'
        except IntegrityError:
            db_session.rollback()

    def test_different_date_allowed(self, app, db_session):
        """測試不同日期可以各有一筆。"""
        price1 = FlightPrice(
            flight_number='CI-100', price=12000,
            scrape_date=date(2026, 4, 1), airline='中華航空',
            origin='TPE', destination='NRT',
        )
        price2 = FlightPrice(
            flight_number='CI-100', price=11500,
            scrape_date=date(2026, 4, 2), airline='中華航空',
            origin='TPE', destination='NRT',
        )
        db_session.add_all([price1, price2])
        db_session.commit()

        assert FlightPrice.query.count() == 2


class TestFetchPriceViaPlaywright:
    """Playwright 爬取函式測試。"""

    @patch('playwright.sync_api.sync_playwright')
    def test_playwright_success(self, mock_pw, app):
        """測試 Playwright 成功從 Google Flights 擷取價格。"""
        mock_locator = MagicMock()
        mock_locator.all_text_contents.return_value = [
            '$5,699', '$5,699', '$8,088', '$12,345',
        ]
        mock_page = MagicMock()
        mock_page.locator.return_value = mock_locator
        mock_browser = MagicMock()
        mock_browser.new_page.return_value = mock_page
        mock_pw_instance = MagicMock()
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_pw.return_value.__enter__ = MagicMock(return_value=mock_pw_instance)
        mock_pw.return_value.__exit__ = MagicMock(return_value=False)

        result = _fetch_price_via_playwright('TPE', 'NRT', date(2026, 5, 1))

        assert result is not None
        assert result['price'] == 5699.0

    @patch('playwright.sync_api.sync_playwright')
    def test_playwright_no_prices(self, mock_pw, app):
        """測試頁面無價格資料時回傳 None。"""
        mock_locator = MagicMock()
        mock_locator.all_text_contents.return_value = ['No results']
        mock_page = MagicMock()
        mock_page.locator.return_value = mock_locator
        mock_browser = MagicMock()
        mock_browser.new_page.return_value = mock_page
        mock_pw_instance = MagicMock()
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_pw.return_value.__enter__ = MagicMock(return_value=mock_pw_instance)
        mock_pw.return_value.__exit__ = MagicMock(return_value=False)

        result = _fetch_price_via_playwright('TPE', 'NRT', date(2026, 5, 1))

        assert result is None

    @patch('playwright.sync_api.sync_playwright')
    def test_playwright_exception(self, mock_pw, app):
        """測試 Playwright 發生例外時回傳 None。"""
        mock_pw.return_value.__enter__ = MagicMock(side_effect=Exception('啟動失敗'))
        mock_pw.return_value.__exit__ = MagicMock(return_value=False)

        result = _fetch_price_via_playwright('TPE', 'NRT', date(2026, 5, 1))

        assert result is None


class TestScrapeChainSwitch:
    """查詢鏈切換邏輯測試。"""

    @patch('app.scraper._fetch_price_from_skyscanner')
    def test_use_api_when_key_set(self, mock_api, app, db_session):
        """測試有 API Key 時使用 API。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        mock_api.return_value = {'price': 12000, 'departure_time': None}

        with patch.dict('os.environ', {'SKYSCANNER_API_KEY': 'test-key'}):
            result = scrape_flight_price(flight)

        assert result is not None
        mock_api.assert_called_once()

    @patch('app.scraper._fetch_price_via_playwright')
    def test_use_playwright_when_no_key(self, mock_pw, app, db_session):
        """測試無 API Key 時使用 Playwright。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        mock_pw.return_value = {'price': 12000, 'departure_time': None}

        with patch.dict('os.environ', {'SKYSCANNER_API_KEY': ''}):
            result = scrape_flight_price(flight)

        assert result is not None
        mock_pw.assert_called_once()
