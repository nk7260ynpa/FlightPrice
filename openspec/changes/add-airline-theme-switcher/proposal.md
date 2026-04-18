## Why

目前 FlightPrice 僅支援單一酷航（Scoot）主題，視覺風格鎖死在 `:root` 的 `--scoot-*` tokens 與 `.scoot-*` class 上。使用者希望能在頁面上即時切換到其他航司品牌主題（長榮、中華、星宇），以展現同一份資料在不同品牌語言下的呈現；同時主題選擇需跨頁面、跨 session 持久化，避免每次重載都退回預設。此變更建立多主題基礎架構，為未來加入更多航司（或使用者自訂）留下擴充點。

## What Changes

- **新增主題切換選單**：於 navbar 加入主題切換 UI（dropdown 或按鈕群組），使用者可即時切換 4 個主題。
- **新增 3 個航空品牌主題**：EVA Air（長榮）、China Airlines（中華）、Starlux（星宇），各自擁有獨立的色票、字體、視覺裝飾。
- **多主題 CSS 架構**：將現有 `:root` 的 `--scoot-*` tokens 拆分到 `:root[data-theme="scoot"]`，並新增 `[data-theme="eva"]`、`[data-theme="china-airlines"]`、`[data-theme="starlux"]` 三個 scope；元件 CSS 改引用中性語意 token（`--theme-primary`、`--theme-ink` 等），達到主題切換即時生效。
- **中性 class 別名**：為元件引入 `.btn-theme`、`.navbar-theme`、`.stat-theme--*`、`.table-theme`、`.badge-theme-*`、`.card-header-theme` 等中性 class；既有 `.*-scoot` class 保留為別名以向下相容，並確保 `tests/test_theme_smoke.py` 現有斷言不破壞。
- **主題持久化**：使用者選定的主題 SHALL 以 `localStorage` 記錄（key：`flightprice-theme`），頁面載入時優先套用；伺服器端首次渲染 SHALL 以預設主題（`scoot`）為準，前端 inline script 在 DOM 可用前覆寫 `<html data-theme>` 以避免 flash。
- **Chart.js 配色改由 theme tokens 讀取**：折線、資料點、tooltip 色彩改自 CSS custom properties 取值，主題切換後圖表重繪同步採新色。
- **測試擴充**：`tests/test_theme_smoke.py` 新增每個主題的 smoke 與切換器 UI／JS 持久化測試。

## Capabilities

### New Capabilities
- `theme-switcher`：多主題架構、主題切換 UI、localStorage 持久化、前端 data-theme 切換機制。
- `eva-theme`：長榮航空品牌 tokens 與元件對應規範。
- `china-airlines-theme`：中華航空品牌 tokens 與元件對應規範。
- `starlux-theme`：星宇航空品牌 tokens 與元件對應規範（含按鈕按壓行為差異化）。

### Modified Capabilities
- `scoot-theme`：現有 `:root` 色彩 tokens 改為 `:root[data-theme="scoot"]` 範圍，元件 CSS 改經由中性語意 token 引用；既有 `.scoot-*` class 保留為別名，視覺不變。

## Impact

- 影響檔案：
  - `app/static/css/style.css`（大幅重構，引入 data-theme scope 與中性 tokens／class）
  - `app/templates/base.html`（navbar 新增主題切換器、`<html data-theme>` 屬性、無閃爍 inline script、字體 `<link>` 擴充以涵蓋 4 主題字型）
  - `app/static/js/theme-switcher.js`（新增，負責讀寫 localStorage 與切換 `data-theme`）
  - `app/templates/charts.html`（Chart.js 配置改讀取 CSS custom properties；主題切換事件觸發重繪）
  - `tests/test_theme_smoke.py`（擴充 4 主題 smoke、切換器渲染、JS 切換行為測試）
- 不影響：資料庫 schema、Scraper、班機／價格業務邏輯、任何 Python route。
- 外部相依：無新增 Python 套件；新增 Google Fonts 請求（Cormorant Garamond、Noto Serif TC、Inter Tight、IBM Plex Mono 等，依 design.md 定義）。
- 向下相容：既有 `.navbar-scoot`、`.btn-scoot`、`.stat-scoot--*`、`.table-scoot`、`.badge-scoot-*` class 全數保留；`tests/test_theme_smoke.py` 現有斷言在預設 scoot 主題下依然通過。
