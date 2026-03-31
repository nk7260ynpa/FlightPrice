"""航班資訊查詢模組（多層備援）單元測試。"""

from datetime import date
from unittest.mock import MagicMock, patch

from app import db
from app.flight_lookup import (
    lookup_flight_info,
    _lookup_from_code_table,
    _lookup_from_db_cache,
    _lookup_via_flightradar24,
)
from app.models import TrackedFlight


class TestDBCacheLookup:
    """DB 快取查詢測試。"""

    def test_cache_hit(self, app, db_session):
        """測試 DB 有同班次紀錄時直接回傳。"""
        flight = TrackedFlight(
            flight_number='TR866', airline='酷航',
            origin='TPE', destination='NRT',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        result = _lookup_from_db_cache('TR866', 'TR866')
        assert result is not None
        assert result['airline'] == '酷航'
        assert result['origin'] == 'TPE'
        assert result['destination'] == 'NRT'

    def test_cache_miss(self, app, db_session):
        """測試 DB 無紀錄時回傳 None。"""
        result = _lookup_from_db_cache('TR866', 'TR866')
        assert result is None

    def test_cache_skip_empty_origin(self, app, db_session):
        """測試 DB 有紀錄但 origin 為空時不命中。"""
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
    def test_fr24_success(self, mock_get, app):
        """測試 Flightradar24 成功解析航線。"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
        <title>TR866 - Scoot Flight Tracker</title>
        <table id="tbl-datatable">
            <tr><th>Date</th><th>From</th><th>To</th></tr>
            <tr>
                <td>2026-03-30</td>
                <td>Taipei (TPE)</td>
                <td>Tokyo Narita (NRT)</td>
            </tr>
        </table>
        </html>
        """
        mock_get.return_value = mock_response

        result = _lookup_via_flightradar24('TR866')
        assert result is not None
        assert result['origin'] == 'TPE'
        assert result['destination'] == 'NRT'
        assert 'Scoot' in result['airline']

    @patch('app.flight_lookup.requests.get')
    def test_fr24_non_200(self, mock_get, app):
        """測試 Flightradar24 回傳非 200 時回傳 None。"""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        result = _lookup_via_flightradar24('TR866')
        assert result is None

    @patch('app.flight_lookup.requests.get')
    def test_fr24_request_exception(self, mock_get, app):
        """測試 Flightradar24 請求失敗時回傳 None。"""
        mock_get.side_effect = Exception('連線逾時')

        result = _lookup_via_flightradar24('TR866')
        assert result is None

    @patch('app.flight_lookup.requests.get')
    def test_fr24_empty_table(self, mock_get, app):
        """測試 Flightradar24 頁面無資料表時回傳 None。"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>No data</body></html>'
        mock_get.return_value = mock_response

        result = _lookup_via_flightradar24('TR866')
        assert result is None


class TestLookupChainOrder:
    """查詢鏈順序測試。"""

    def test_db_cache_first(self, app, db_session):
        """測試 DB 快取為第一優先，命中時不呼叫外部 API。"""
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

            assert result is not None
            assert result['origin'] == 'TPE'
            mock_fr24.assert_not_called()
            mock_avs.assert_not_called()

    @patch('app.flight_lookup._lookup_via_flightradar24')
    def test_fr24_second(self, mock_fr24, app, db_session):
        """測試 DB 無快取時使用 Flightradar24。"""
        mock_fr24.return_value = {
            'airline': '酷航', 'origin': 'TPE', 'destination': 'NRT',
        }

        with patch('app.flight_lookup._lookup_via_aviationstack') as mock_avs:
            result = lookup_flight_info('TR866')

            assert result is not None
            assert result['origin'] == 'TPE'
            mock_fr24.assert_called_once()
            mock_avs.assert_not_called()

    @patch('app.flight_lookup._lookup_via_flightradar24', return_value=None)
    @patch('app.flight_lookup._lookup_via_aviationstack')
    def test_aviationstack_third(self, mock_avs, mock_fr24, app, db_session):
        """測試 Flightradar24 失敗時使用 AviationStack。"""
        mock_avs.return_value = {
            'airline': 'Scoot', 'origin': 'TPE', 'destination': 'NRT',
        }

        result = lookup_flight_info('TR866')

        assert result is not None
        mock_fr24.assert_called_once()
        mock_avs.assert_called_once()

    @patch('app.flight_lookup._lookup_via_flightradar24', return_value=None)
    @patch('app.flight_lookup._lookup_via_aviationstack', return_value=None)
    def test_iata_table_last(self, mock_avs, mock_fr24, app, db_session):
        """測試所有外部來源失敗時使用 IATA 對照表。"""
        result = lookup_flight_info('CI100')

        assert result is not None
        assert result['airline'] == '中華航空'
        assert result['origin'] == ''
        assert result['destination'] == ''

    @patch('app.flight_lookup._lookup_via_flightradar24', return_value=None)
    @patch('app.flight_lookup._lookup_via_aviationstack', return_value=None)
    def test_all_fail(self, mock_avs, mock_fr24, app, db_session):
        """測試所有來源皆失敗時回傳 None。"""
        result = lookup_flight_info('XX999')

        assert result is None


class TestCodeTableLookup:
    """IATA 代碼對照表測試。"""

    def test_known_airline(self, app):
        """測試已知航空公司代碼。"""
        result = _lookup_from_code_table('TR866')
        assert result is not None
        assert result['airline'] == '酷航'
        assert result['origin'] == ''

    def test_unknown_airline(self, app):
        """測試未知航空公司代碼。"""
        result = _lookup_from_code_table('XX999')
        assert result is None
