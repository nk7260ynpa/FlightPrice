"""酷航主題渲染 smoke 測試。

目的：驗證 4 個模板與靜態 CSS 檔確實套用 scoot-theme，
並確保舊 aviation-theme 的 class 字串完全移除。
"""

from datetime import date, datetime

import pytest

from app import db
from app.models import ScrapeLog, TrackedFlight


# 舊主題遺留字串：若任一字串於 HTML 或 CSS 出現即視為 regression。
OLD_AVIATION_MARKERS = (
    'navbar-aviation',
    'btn-aviation',
    'table-aviation',
    'stat-card-stripe',
    'stat-card-value',
    'stat-card-label',
    'stat-card-content',
    'badge-aviation-',
    '--av-',
)


def _assert_no_aviation(text: str) -> None:
    """斷言文字內容不得出現任何舊 aviation 主題標記。"""
    for marker in OLD_AVIATION_MARKERS:
        assert marker not in text, f'發現殘留舊主題 class: {marker!r}'


class TestFlightsPageScootTheme:
    """班機管理頁（GET /）酷航主題渲染驗證。"""

    def test_navbar_scoot_class_present(self, client):
        """/ 回應 HTML 中應出現 navbar-scoot class。"""
        response = client.get('/')
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'navbar-scoot' in html

    def test_primary_button_uses_btn_scoot(self, client):
        """「新增」主按鈕的 btn-scoot class 應出現在 / 回應中。"""
        response = client.get('/')
        html = response.data.decode('utf-8')
        assert 'btn-scoot' in html

    def test_flights_page_has_no_aviation_markers(self, client, db_session):
        """即使有追蹤班機，/ 回應仍不得包含舊 aviation class。"""
        flight = TrackedFlight(
            flight_number='TR-872',
            airline='Scoot',
            origin='TPE',
            destination='SIN',
            departure_date=date(2026, 6, 1),
        )
        db_session.add(flight)
        db_session.commit()

        response = client.get('/')
        html = response.data.decode('utf-8')
        # 同時驗證 scoot class 實際出現於清單區塊。
        assert 'table-scoot' in html
        assert 'badge-scoot-success' in html
        _assert_no_aviation(html)


class TestChartsPageScootTheme:
    """價格圖表頁（GET /charts）酷航主題渲染驗證。"""

    def test_stat_scoot_variants_present_when_flight_selected(
        self, client, db_session,
    ):
        """當選取班機時，三張 stat-scoot 變體應全數出現。"""
        flight = TrackedFlight(
            flight_number='TR-993',
            airline='Scoot',
            origin='KIX',
            destination='SIN',
            departure_date=date(2026, 7, 1),
        )
        db_session.add(flight)
        db_session.commit()

        response = client.get(f'/charts?flight_id={flight.id}')
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'stat-scoot--danger' in html
        assert 'stat-scoot--success' in html
        assert 'stat-scoot--ink' in html
        _assert_no_aviation(html)

    def test_charts_empty_state_has_no_aviation(self, client):
        """未選取班機時的空狀態頁亦不得含舊 class。"""
        response = client.get('/charts')
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        _assert_no_aviation(html)


class TestStatusPageScootTheme:
    """抓取狀態頁（GET /status）酷航主題渲染驗證。"""

    def test_status_page_uses_scoot_classes(self, client, db_session):
        """有抓取紀錄時，table-scoot 與 badge-scoot-success 應出現。"""
        flight = TrackedFlight(
            flight_number='TR-101',
            airline='Scoot',
            origin='TPE',
            destination='MFM',
            departure_date=date(2026, 5, 1),
        )
        db_session.add(flight)
        db_session.commit()

        log = ScrapeLog(
            flight_number=flight.flight_number,
            status='success',
            price=3200.0,
            scraped_at=datetime.now(),
        )
        db_session.add(log)
        db_session.commit()

        response = client.get('/status')
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'table-scoot' in html
        assert 'badge-scoot-success' in html
        _assert_no_aviation(html)

    def test_status_primary_cta_is_btn_scoot_danger(self, client):
        """「立即抓取」按鈕應為 btn-scoot-danger。"""
        response = client.get('/status')
        html = response.data.decode('utf-8')
        assert 'btn-scoot-danger' in html
        _assert_no_aviation(html)


class TestStaticCssFile:
    """靜態 CSS 檔案內容驗證。"""

    def test_style_css_is_served_with_correct_content_type(self, client):
        """/static/css/style.css 應回應 200 且 Content-Type 為 text/css。"""
        response = client.get('/static/css/style.css')
        assert response.status_code == 200
        content_type = response.headers.get('Content-Type', '')
        assert 'text/css' in content_type

    def test_style_css_contains_scoot_yellow_token(self, client):
        """style.css 應包含 --scoot-yellow: #FFDA00 token 宣告。"""
        response = client.get('/static/css/style.css')
        css_text = response.data.decode('utf-8')
        assert '--scoot-yellow' in css_text
        assert '#FFDA00' in css_text

    def test_style_css_has_no_aviation_remnants(self, client):
        """style.css 不得包含 --av- 或 aviation 字串。"""
        response = client.get('/static/css/style.css')
        css_text = response.data.decode('utf-8')
        assert '--av-' not in css_text
        assert 'aviation' not in css_text


class TestBaseTemplateFonts:
    """base.html 字體與骨架驗證。"""

    def test_google_fonts_preconnect_present(self, client):
        """base.html 應 preconnect 至 Google Fonts。"""
        response = client.get('/')
        html = response.data.decode('utf-8')
        assert 'fonts.googleapis.com' in html
        assert 'fonts.gstatic.com' in html

    def test_fonts_link_includes_scoot_fonts(self, client):
        """字體 <link> 應包含 Nunito、Nunito Sans 與 JetBrains Mono。"""
        response = client.get('/')
        html = response.data.decode('utf-8')
        assert 'Nunito' in html
        assert 'JetBrains+Mono' in html
