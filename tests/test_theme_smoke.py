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


# --------------------------------------------------------------------------- #
# 多主題切換器（add-airline-theme-switcher）相關測試
# --------------------------------------------------------------------------- #


THEME_SWITCHER_PAGES = ('/', '/charts', '/status')


class TestThemeSwitcherUI:
    """主題切換器 UI 於所有頁面渲染驗證。"""

    @pytest.mark.parametrize('path', THEME_SWITCHER_PAGES)
    def test_switcher_button_has_aria_label(self, client, path):
        """切換按鈕 MUST 具備 aria-label="主題切換"。"""
        response = client.get(path)
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'aria-label="主題切換"' in html

    @pytest.mark.parametrize('path', THEME_SWITCHER_PAGES)
    def test_switcher_lists_four_themes(self, client, path):
        """下拉選單 MUST 同時列出四個 data-theme-value 選項。"""
        response = client.get(path)
        html = response.data.decode('utf-8')
        assert 'data-theme-value="scoot"' in html
        assert 'data-theme-value="eva"' in html
        assert 'data-theme-value="china-airlines"' in html
        assert 'data-theme-value="starlux"' in html

    @pytest.mark.parametrize('path', THEME_SWITCHER_PAGES)
    def test_switcher_shows_traditional_chinese_labels(self, client, path):
        """選項 MUST 顯示繁體中文品牌名（酷航 / 長榮 / 中華 / 星宇）。"""
        response = client.get(path)
        html = response.data.decode('utf-8')
        assert '酷航' in html
        assert '長榮航空' in html
        assert '中華航空' in html
        assert '星宇航空' in html

    def test_switcher_current_option_has_aria_current(self, client):
        """載入時 scoot 選項 MUST 以 aria-current="true" 標示為啟用。"""
        response = client.get('/')
        html = response.data.decode('utf-8')
        # scoot 為預設主題；HTML 中相關 <button> 內應同時存在
        # data-theme-value="scoot" 與 aria-current="true"
        assert 'aria-current="true"' in html


class TestThemeSwitcherScript:
    """theme-switcher.js 靜態資源與內容驗證。"""

    def test_script_served_with_200_and_js_content_type(self, client):
        """/static/js/theme-switcher.js 應回應 200，Content-Type 含 javascript。"""
        response = client.get('/static/js/theme-switcher.js')
        assert response.status_code == 200
        content_type = response.headers.get('Content-Type', '')
        assert 'javascript' in content_type.lower()

    def test_script_contains_required_symbols(self, client):
        """原始碼 MUST 含 flightprice-theme / data-theme-value / themechange 與白名單。"""
        response = client.get('/static/js/theme-switcher.js')
        js_text = response.data.decode('utf-8')
        assert 'flightprice-theme' in js_text
        assert 'data-theme-value' in js_text
        assert 'themechange' in js_text
        # 四主題白名單字串需全數出現
        assert "'scoot'" in js_text
        assert "'eva'" in js_text
        assert "'china-airlines'" in js_text
        assert "'starlux'" in js_text

    def test_script_must_not_reload_page(self, client):
        """原始碼 MUST NOT 呼叫 location.reload（切換不得刷新頁面）。"""
        response = client.get('/static/js/theme-switcher.js')
        js_text = response.data.decode('utf-8')
        assert 'location.reload' not in js_text
        assert 'window.location.reload' not in js_text


class TestBaseTemplateFOUC:
    """base.html 首屏 FOUC 防護 inline script 驗證。"""

    def test_fouc_script_appears_before_bootstrap_css(self, client):
        """FOUC inline script MUST 出現在 bootstrap.min.css <link> 之前。"""
        response = client.get('/')
        html = response.data.decode('utf-8')
        # 尋找 inline script 與 Bootstrap CSS link 的位置
        bootstrap_idx = html.find('bootstrap.min.css')
        script_idx = html.find('flightprice-theme')
        assert bootstrap_idx != -1, 'Bootstrap CSS link 不存在'
        assert script_idx != -1, 'FOUC script 不存在'
        assert script_idx < bootstrap_idx, (
            'FOUC inline script 必須出現在 bootstrap.min.css 之前'
        )

    def test_fouc_script_contains_required_tokens(self, client):
        """inline script MUST 包含 flightprice-theme / data-theme / try。"""
        response = client.get('/')
        html = response.data.decode('utf-8')
        assert 'flightprice-theme' in html
        assert 'data-theme' in html
        assert 'try' in html

    def test_fouc_script_appears_before_style_css(self, client):
        """FOUC inline script MUST 出現在 style.css <link> 之前。"""
        response = client.get('/')
        html = response.data.decode('utf-8')
        style_idx = html.find('css/style.css')
        script_idx = html.find('flightprice-theme')
        assert style_idx != -1
        assert script_idx < style_idx


class TestEvaThemeCss:
    """style.css 中 EVA 主題規則驗證。"""

    def test_eva_scope_present(self, client):
        """CSS MUST 包含 :root[data-theme="eva"] selector。"""
        response = client.get('/static/css/style.css')
        css_text = response.data.decode('utf-8')
        assert ':root[data-theme="eva"]' in css_text

    def test_eva_brand_colors_present(self, client):
        """EVA 主色 #005F3C 與金色 #D4A84B MUST 出現於 CSS。"""
        response = client.get('/static/css/style.css')
        css_text = response.data.decode('utf-8')
        assert '#005F3C' in css_text
        assert '#D4A84B' in css_text

    def test_eva_font_families_present(self, client):
        """EVA 字體 Noto Serif TC / Source Sans 3 MUST 出現於 CSS。"""
        response = client.get('/static/css/style.css')
        css_text = response.data.decode('utf-8')
        assert 'Noto Serif TC' in css_text
        assert 'Source Sans 3' in css_text


class TestChinaAirlinesThemeCss:
    """style.css 中 China Airlines 主題規則驗證。"""

    def test_cal_scope_present(self, client):
        """CSS MUST 包含 :root[data-theme="china-airlines"] selector。"""
        response = client.get('/static/css/style.css')
        css_text = response.data.decode('utf-8')
        assert ':root[data-theme="china-airlines"]' in css_text

    def test_cal_brand_colors_present(self, client):
        """CAL 主色 #003F87 與 CI 紅 #C8102E MUST 出現於 CSS。"""
        response = client.get('/static/css/style.css')
        css_text = response.data.decode('utf-8')
        assert '#003F87' in css_text
        assert '#C8102E' in css_text


class TestStarluxThemeCss:
    """style.css 中 Starlux 主題規則驗證。"""

    def test_starlux_scope_present(self, client):
        """CSS MUST 包含 :root[data-theme="starlux"] selector。"""
        response = client.get('/static/css/style.css')
        css_text = response.data.decode('utf-8')
        assert ':root[data-theme="starlux"]' in css_text

    def test_starlux_brand_colors_present(self, client):
        """星宇午夜藍 #0E1842 與香檳金 #C8A96A MUST 出現於 CSS。"""
        response = client.get('/static/css/style.css')
        css_text = response.data.decode('utf-8')
        assert '#0E1842' in css_text
        assert '#C8A96A' in css_text

    def test_starlux_font_families_present(self, client):
        """星宇字體 Cormorant Garamond / Inter Tight MUST 出現於 CSS。"""
        response = client.get('/static/css/style.css')
        css_text = response.data.decode('utf-8')
        assert 'Cormorant Garamond' in css_text
        assert 'Inter Tight' in css_text

    def test_starlux_btn_press_width_zero(self, client):
        """Starlux scope 內 --theme-btn-press-width: 0px MUST 存在。"""
        response = client.get('/static/css/style.css')
        css_text = response.data.decode('utf-8')
        assert '--theme-btn-press-width: 0px' in css_text


class TestChartsThemeIntegration:
    """charts.html Chart.js 與主題整合驗證。"""

    def test_charts_html_reads_theme_tokens(self, client, db_session):
        """charts.html MUST 透過 getPropertyValue('--theme- 動態讀取色。"""
        flight = TrackedFlight(
            flight_number='TR-555',
            airline='Scoot',
            origin='TPE',
            destination='SIN',
            departure_date=date(2026, 9, 1),
        )
        db_session.add(flight)
        db_session.commit()

        response = client.get(f'/charts?flight_id={flight.id}')
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert "getPropertyValue('--theme-" in html
        assert 'themechange' in html

    def test_charts_html_removes_hardcoded_scoot_colors(self, client, db_session):
        """Chart.js 配置內 MUST NOT 出現硬編 '#0E0E10' 或 '#FFDA00'。"""
        flight = TrackedFlight(
            flight_number='TR-777',
            airline='Scoot',
            origin='TPE',
            destination='KIX',
            departure_date=date(2026, 10, 1),
        )
        db_session.add(flight)
        db_session.commit()

        response = client.get(f'/charts?flight_id={flight.id}')
        html = response.data.decode('utf-8')
        # 硬編 hex 色碼字串 MUST 不出現（允許 fallback 於 JS 函式內，
        # 但本 spec 要求 Chart.js dataset 與 options 不得硬編，
        # 以下斷言檢查完整硬編 literal 字串是否出現。）
        assert "'#0E0E10'" not in html
        assert "'#FFDA00'" not in html
        assert "'rgba(14, 14, 16, 0.08)'" not in html


class TestNeutralClassAliases:
    """中性 class 別名與既有 scoot class 並存驗證。"""

    def test_neutral_and_scoot_classes_coexist(self, client):
        """style.css MUST 同時包含 .*-theme* 與 .*-scoot* 別名。"""
        response = client.get('/static/css/style.css')
        css_text = response.data.decode('utf-8')

        # 中性 class
        assert '.navbar-theme' in css_text
        assert '.btn-theme' in css_text
        assert '.btn-theme-danger' in css_text
        assert '.stat-theme' in css_text
        assert '.stat-theme--ink' in css_text
        assert '.table-theme' in css_text
        assert '.badge-theme-success' in css_text

        # 既有 scoot 別名必須仍存在
        assert '.navbar-scoot' in css_text
        assert '.btn-scoot' in css_text
        assert '.btn-scoot-danger' in css_text
        assert '.stat-scoot' in css_text
        assert '.stat-scoot--ink' in css_text
        assert '.table-scoot' in css_text
        assert '.badge-scoot-success' in css_text
