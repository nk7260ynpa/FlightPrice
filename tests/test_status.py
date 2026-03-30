"""抓取狀態路由單元測試。"""

from datetime import date

from app import db
from app.models import ScrapeLog, TrackedFlight


class TestStatusIndex:
    """抓取狀態頁面測試。"""

    def test_status_page_no_logs(self, client):
        """測試今日無抓取紀錄時顯示提示。"""
        response = client.get('/status')
        assert response.status_code == 200
        assert '今日尚未執行抓取' in response.data.decode('utf-8')

    def test_status_page_with_success_log(self, client, db_session):
        """測試有成功紀錄時顯示統計與表格。"""
        flight = TrackedFlight(
            flight_number='CI-100', airline='中華航空',
            origin='TPE', destination='NRT', is_active=True,
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        log = ScrapeLog(
            flight_number='CI-100', status='success', price=12500,
        )
        db_session.add(log)
        db_session.commit()

        response = client.get('/status')
        html = response.data.decode('utf-8')
        assert response.status_code == 200
        assert 'CI-100' in html
        assert '成功' in html

    def test_status_page_with_failed_log(self, client, db_session):
        """測試有失敗紀錄時顯示錯誤原因。"""
        log = ScrapeLog(
            flight_number='CI-100', status='failed',
            error_message='連線逾時',
        )
        db_session.add(log)
        db_session.commit()

        response = client.get('/status')
        html = response.data.decode('utf-8')
        assert '失敗' in html
        assert '連線逾時' in html

    def test_status_page_statistics(self, client, db_session):
        """測試統計數字正確顯示。"""
        for i in range(2):
            flight = TrackedFlight(
                flight_number=f'CI-{i}', airline='中華航空',
                origin='TPE', destination='NRT', is_active=True,
                departure_date=date(2026, 5, 1),
            )
            db_session.add(flight)
        db_session.commit()

        db_session.add(ScrapeLog(
            flight_number='CI-0', status='success', price=10000,
        ))
        db_session.add(ScrapeLog(
            flight_number='CI-1', status='failed',
            error_message='API 錯誤',
        ))
        db_session.commit()

        response = client.get('/status')
        html = response.data.decode('utf-8')
        assert response.status_code == 200
        # 統計區塊應出現在頁面中
        assert '追蹤班機數' in html
        assert '成功擷取' in html
        assert '失敗擷取' in html
