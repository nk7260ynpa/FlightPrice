"""價格圖表路由單元測試。"""

import json
from datetime import date

from app import db
from app.models import FlightPrice, TrackedFlight


class TestChartsIndex:
    """圖表頁面測試。"""

    def test_charts_page_loads(self, client):
        """測試圖表頁面正常載入。"""
        response = client.get('/charts')
        assert response.status_code == 200
        assert '價格趨勢圖表' in response.data.decode('utf-8')

    def test_charts_page_with_flight_selected(self, client, db_session):
        """測試選擇班機後頁面載入。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT',
        )
        db_session.add(flight)
        db_session.commit()

        response = client.get(f'/charts?flight_id={flight.id}')
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'priceChart' in html


class TestChartDataAPI:
    """圖表資料 API 測試。"""

    def _setup_flight_with_prices(self, db_session):
        """建立測試用班機與價格資料。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT',
        )
        db_session.add(flight)
        db_session.commit()

        for i, price_val in enumerate([10000, 12000, 11000]):
            price = FlightPrice(
                flight_number='CI-100',
                price=price_val,
                scrape_date=date(2026, 3, 28 + i),
                airline='中華航空',
                origin='TPE',
                destination='NRT',
                tracked_flight_id=flight.id,
            )
            db_session.add(price)
        db_session.commit()
        return flight

    def test_chart_data_with_prices(self, client, db_session):
        """測試有價格資料時回傳正確 JSON。"""
        flight = self._setup_flight_with_prices(db_session)

        response = client.get(f'/api/charts/{flight.id}')
        data = json.loads(response.data)

        assert len(data['labels']) == 3
        assert len(data['data']) == 3
        assert data['stats']['max'] == 12000.0
        assert data['stats']['min'] == 10000.0
        assert data['stats']['avg'] == 11000.0

    def test_chart_data_no_prices(self, client, db_session):
        """測試無價格資料時回傳空結果。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT',
        )
        db_session.add(flight)
        db_session.commit()

        response = client.get(f'/api/charts/{flight.id}')
        data = json.loads(response.data)

        assert data['labels'] == []
        assert data['data'] == []
        assert data['stats'] is None

    def test_chart_data_nonexistent_flight(self, client):
        """測試不存在的班機回傳 404。"""
        response = client.get('/api/charts/999')
        assert response.status_code == 404
