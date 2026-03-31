"""航班資訊查詢模組（多層備援 + 多段航班）單元測試。"""

from datetime import date
from unittest.mock import MagicMock, patch

from app import db
from app.flight_lookup import (
    lookup_flight_info,
    _lookup_from_code_table,
    _lookup_from_db_cache,
    _lookup_via_flightradar24,
    _extract_fr24_routes,
)
from app.models import TrackedFlight


class TestDBCacheLookup:
    """DB 快取查詢測試。"""

    def test_cache_hit_returns_list(self, app, db_session):
        """測試 DB 快取命中回傳航段列表。"""
        flight = TrackedFlight(
            flight_number='TR866', airline='酷航',
            origin='TPE', destination='NRT',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        result = _lookup_from_db_cache('TR866', 'TR866')
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['airline'] == '酷航'
        assert result[0]['origin'] == 'TPE'

    def test_cache_miss(self, app, db_session):
        """測試 DB 無紀錄時回傳 None。"""
        result = _lookup_from_db_cache('TR866', 'TR866')
        assert result is None

    def test_cache_skip_empty_origin(self, app, db_session):
        """測試 origin 為空時不命中。"""
        flight = TrackedFlight(
            flight_number='TR866', airline='酷航',
            origin='', destination='',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        result = _lookup_from_db_cache('TR866', 'TR866')
        assert result is None


class TestFlightradar24Lookup:
    """Flightradar24 爬取測試。"""

    @patch('app.flight_lookup.requests.get')
    def test_fr24_single_route(self, mock_get, app):
        """測試單段航班回傳長度 1 列表。"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
        <title>CI100 - China Airlines Flight Tracker</title>
        <table id="tbl-datatable">
            <tr><th>Date</th><th>From</th><th>To</th></tr>
            <tr><td>2026-03-30</td><td>Taipei (TPE)</td><td>Tokyo Narita (NRT)</td></tr>
            <tr><td>2026-03-29</td><td>Taipei (TPE)</td><td>Tokyo Narita (NRT)</td></tr>
        </table>
        </html>
        """
        mock_get.return_value = mock_response

        result = _lookup_via_flightradar24('CI100')
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['origin'] == 'TPE'
        assert result[0]['destination'] == 'NRT'

    @patch('app.flight_lookup.requests.get')
    def test_fr24_multi_route(self, mock_get, app):
        """測試多段航班回傳多個航段。"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
        <title>TR866 - Scoot Flight Tracker</title>
        <table id="tbl-datatable">
            <tr><th>Date</th><th>From</th><th>To</th></tr>
            <tr><td>2026-03-30</td><td>Singapore (SIN)</td><td>Taipei (TPE)</td></tr>
            <tr><td>2026-03-30</td><td>Taipei (TPE)</td><td>Tokyo Narita (NRT)</td></tr>
            <tr><td>2026-03-29</td><td>Singapore (SIN)</td><td>Taipei (TPE)</td></tr>
            <tr><td>2026-03-29</td><td>Taipei (TPE)</td><td>Tokyo Narita (NRT)</td></tr>
        </table>
        </html>
        """
        mock_get.return_value = mock_response

        result = _lookup_via_flightradar24('TR866')
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['origin'] == 'SIN'
        assert result[0]['destination'] == 'TPE'
        assert result[1]['origin'] == 'TPE'
        assert result[1]['destination'] == 'NRT'

    @patch('app.flight_lookup.requests.get')
    def test_fr24_non_200(self, mock_get, app):
        """測試非 200 回傳 None。"""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        result = _lookup_via_flightradar24('TR866')
        assert result is None

    @patch('app.flight_lookup.requests.get')
    def test_fr24_empty_table(self, mock_get, app):
        """測試無資料表時回傳 None。"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>No data</body></html>'
        mock_get.return_value = mock_response

        result = _lookup_via_flightradar24('TR866')
        assert result is None


class TestLookupChainOrder:
    """查詢鏈順序測試。"""

    def test_db_cache_first(self, app, db_session):
        """測試 DB 快取優先，命中時不呼叫外部。"""
        flight = TrackedFlight(
            flight_number='CI100', airline='中華航空',
            origin='TPE', destination='NRT',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        with patch('app.flight_lookup._lookup_via_flightradar24') as mock_fr24, \
             patch('app.flight_lookup._lookup_via_aviationstack') as mock_avs:
            result = lookup_flight_info('CI100')

            assert isinstance(result, list)
            assert result[0]['origin'] == 'TPE'
            mock_fr24.assert_not_called()
            mock_avs.assert_not_called()

    @patch('app.flight_lookup._lookup_via_flightradar24')
    def test_fr24_second(self, mock_fr24, app, db_session):
        """測試 DB 無快取時使用 Flightradar24。"""
        mock_fr24.return_value = [
            {'airline': '酷航', 'origin': 'SIN', 'destination': 'TPE'},
            {'airline': '酷航', 'origin': 'TPE', 'destination': 'NRT'},
        ]

        with patch('app.flight_lookup._lookup_via_aviationstack') as mock_avs:
            result = lookup_flight_info('TR866')

            assert len(result) == 2
            mock_fr24.assert_called_once()
            mock_avs.assert_not_called()

    @patch('app.flight_lookup._lookup_via_flightradar24', return_value=None)
    @patch('app.flight_lookup._lookup_via_aviationstack')
    def test_aviationstack_third(self, mock_avs, mock_fr24, app, db_session):
        """測試 FR24 失敗時用 AviationStack。"""
        mock_avs.return_value = [
            {'airline': 'Scoot', 'origin': 'TPE', 'destination': 'NRT'},
        ]

        result = lookup_flight_info('TR866')
        assert isinstance(result, list)
        assert len(result) == 1

    @patch('app.flight_lookup._lookup_via_flightradar24', return_value=None)
    @patch('app.flight_lookup._lookup_via_aviationstack', return_value=None)
    def test_iata_table_last(self, mock_avs, mock_fr24, app, db_session):
        """測試所有外部來源失敗時用 IATA 對照表。"""
        result = lookup_flight_info('CI100')
        assert isinstance(result, list)
        assert result[0]['airline'] == '中華航空'
        assert result[0]['origin'] == ''

    @patch('app.flight_lookup._lookup_via_flightradar24', return_value=None)
    @patch('app.flight_lookup._lookup_via_aviationstack', return_value=None)
    def test_all_fail(self, mock_avs, mock_fr24, app, db_session):
        """測試全部失敗回傳 None。"""
        result = lookup_flight_info('XX999')
        assert result is None


class TestCodeTableLookup:
    """IATA 代碼對照表測試。"""

    def test_known_airline_returns_list(self, app):
        """測試已知航空公司回傳列表。"""
        result = _lookup_from_code_table('TR866')
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['airline'] == '酷航'

    def test_unknown_airline(self, app):
        """測試未知航空公司回傳 None。"""
        result = _lookup_from_code_table('XX999')
        assert result is None
