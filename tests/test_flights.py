"""班機管理路由單元測試。"""

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
            'airline': '中華航空',
            'origin': 'TPE',
            'destination': 'NRT',
        }, follow_redirects=True)

        assert response.status_code == 200
        assert '已新增追蹤班機 CI-100' in response.data.decode('utf-8')

        flight = TrackedFlight.query.filter_by(flight_number='CI-100').first()
        assert flight is not None

    def test_add_flight_duplicate(self, client, db_session):
        """測試新增重複班次。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT',
        )
        db_session.add(flight)
        db_session.commit()

        response = client.post('/flights/add', data={
            'flight_number': 'CI-100',
            'airline': '中華航空',
            'origin': 'TPE',
            'destination': 'NRT',
        }, follow_redirects=True)

        html = response.data.decode('utf-8')
        assert '該班次已在追蹤清單中' in html

    def test_add_flight_missing_fields(self, client):
        """測試必填欄位未填。"""
        response = client.post('/flights/add', data={
            'flight_number': '',
            'airline': '中華航空',
            'origin': 'TPE',
            'destination': 'NRT',
        }, follow_redirects=True)

        html = response.data.decode('utf-8')
        assert '班次編號為必填欄位' in html


class TestToggleFlight:
    """切換班機狀態測試。"""

    def test_toggle_deactivate(self, client, db_session):
        """測試停用班機。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT', is_active=True,
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
        )
        db_session.add(flight)
        db_session.commit()

        response = client.post(
            f'/flights/{flight.id}/toggle', follow_redirects=True
        )

        assert response.status_code == 200
        updated = db_session.get(TrackedFlight, flight.id)
        assert updated.is_active is True
