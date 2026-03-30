"""班機管理路由單元測試。"""

import json
from datetime import date
from unittest.mock import patch

from app import db
from app.models import TrackedFlight


class TestFlightsIndex:
    """班機清單頁面測試。"""

    def test_index_empty(self, client):
        """測試無追蹤班機時顯示提示訊息。"""
        response = client.get('/')
        assert response.status_code == 200
        assert '尚無追蹤班機' in response.data.decode('utf-8')

    def test_index_with_flights(self, client, db_session):
        """測試有追蹤班機時顯示清單。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        response = client.get('/')
        html = response.data.decode('utf-8')
        assert 'CI-100' in html
        assert '中華航空' in html


class TestAddFlight:
    """新增追蹤班機測試。"""

    def test_add_flight_success(self, client, db_session):
        """測試成功新增班機。"""
        response = client.post('/flights/add', data={
            'flight_number': 'CI-100',
            'departure_date': '2026-05-01',
            'airline': '中華航空',
            'origin': 'TPE',
            'destination': 'NRT',
        }, follow_redirects=True)

        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert '已新增追蹤班機 CI-100' in html

        flight = TrackedFlight.query.filter_by(flight_number='CI-100').first()
        assert flight is not None
        assert flight.departure_date == date(2026, 5, 1)

    def test_add_flight_duplicate(self, client, db_session):
        """測試新增重複班次（同班次 + 同出發日期）。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        response = client.post('/flights/add', data={
            'flight_number': 'CI-100',
            'departure_date': '2026-05-01',
            'airline': '中華航空',
            'origin': 'TPE',
            'destination': 'NRT',
        }, follow_redirects=True)

        html = response.data.decode('utf-8')
        assert '已在追蹤清單中' in html

    def test_add_flight_same_number_different_date(self, client, db_session):
        """測試同班次不同出發日期可新增。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        response = client.post('/flights/add', data={
            'flight_number': 'CI-100',
            'departure_date': '2026-05-15',
            'airline': '中華航空',
            'origin': 'TPE',
            'destination': 'NRT',
        }, follow_redirects=True)

        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert '已新增追蹤班機 CI-100' in html

        flights = TrackedFlight.query.filter_by(flight_number='CI-100').all()
        assert len(flights) == 2

    def test_add_flight_missing_flight_number(self, client):
        """測試班次代碼未填。"""
        response = client.post('/flights/add', data={
            'flight_number': '',
            'departure_date': '2026-05-01',
            'airline': '中華航空',
            'origin': 'TPE',
            'destination': 'NRT',
        }, follow_redirects=True)

        html = response.data.decode('utf-8')
        assert '班次代碼為必填欄位' in html

    def test_add_flight_missing_departure_date(self, client):
        """測試出發日期未填。"""
        response = client.post('/flights/add', data={
            'flight_number': 'CI-100',
            'departure_date': '',
            'airline': '中華航空',
            'origin': 'TPE',
            'destination': 'NRT',
        }, follow_redirects=True)

        html = response.data.decode('utf-8')
        assert '出發日期為必填欄位' in html

    def test_add_flight_invalid_departure_date(self, client):
        """測試出發日期格式錯誤。"""
        response = client.post('/flights/add', data={
            'flight_number': 'CI-100',
            'departure_date': 'not-a-date',
            'airline': '中華航空',
            'origin': 'TPE',
            'destination': 'NRT',
        }, follow_redirects=True)

        html = response.data.decode('utf-8')
        assert '出發日期格式錯誤' in html

    def test_add_flight_missing_airline_origin_destination(self, client):
        """測試航空公司、出發地、抵達地未填。"""
        response = client.post('/flights/add', data={
            'flight_number': 'CI-100',
            'departure_date': '2026-05-01',
            'airline': '',
            'origin': '',
            'destination': '',
        }, follow_redirects=True)

        html = response.data.decode('utf-8')
        assert '航空公司、出發地、抵達地皆為必填' in html


class TestToggleFlight:
    """切換班機狀態測試。"""

    def test_toggle_deactivate(self, client, db_session):
        """測試停用班機。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT', is_active=True,
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        response = client.post(
            f'/flights/{flight.id}/toggle', follow_redirects=True
        )

        assert response.status_code == 200
        updated = db_session.get(TrackedFlight, flight.id)
        assert updated.is_active is False

    def test_toggle_activate(self, client, db_session):
        """測試重新啟用班機。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT', is_active=False,
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        response = client.post(
            f'/flights/{flight.id}/toggle', follow_redirects=True
        )

        assert response.status_code == 200
        updated = db_session.get(TrackedFlight, flight.id)
        assert updated.is_active is True


class TestFlightLookupAPI:
    """航班資訊查詢 API 測試。"""

    def test_lookup_missing_flight_number(self, client):
        """測試未提供班次代碼時回傳 400。"""
        response = client.get('/api/flights/lookup')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert '請輸入班次代碼' in data['error']

    def test_lookup_empty_flight_number(self, client):
        """測試提供空白班次代碼時回傳 400。"""
        response = client.get('/api/flights/lookup?flight_number=')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert '請輸入班次代碼' in data['error']

    @patch('app.routes.flights.lookup_flight_info')
    def test_lookup_found(self, mock_lookup, client):
        """測試成功查詢航班資訊。"""
        mock_lookup.return_value = {
            'airline': '中華航空',
            'origin': 'TPE',
            'destination': 'NRT',
        }

        response = client.get('/api/flights/lookup?flight_number=CI100')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['airline'] == '中華航空'
        assert data['origin'] == 'TPE'
        assert data['destination'] == 'NRT'

    @patch('app.routes.flights.lookup_flight_info')
    def test_lookup_not_found(self, mock_lookup, client):
        """測試查詢不到航班資訊時回傳 404。"""
        mock_lookup.return_value = None

        response = client.get('/api/flights/lookup?flight_number=XX999')
        data = json.loads(response.data)

        assert response.status_code == 404
        assert '無法查詢該班次資訊' in data['error']
