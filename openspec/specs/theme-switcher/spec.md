### Requirement: 多主題架構（data-theme 屬性 + 中性語意 tokens）

系統 SHALL 在 `app/static/css/style.css` 中以 `<html data-theme="...">` 屬性為主題切換開關，支援以下四個有效值且不得多於此：`scoot`、`eva`、`china-airlines`、`starlux`。每個 data-theme 值 MUST 對應一組 CSS 自訂屬性 scope（`:root[data-theme="<value>"] { ... }`），於該 scope 中映射中性語意 tokens。

中性語意 tokens SHALL 至少包含以下名稱（元件 CSS MUST 只引用這組中性 tokens，不得在元件規則中直接引用 `--scoot-*` / `--eva-*` / `--cal-*` / `--jx-*` 品牌專屬 token）：

- 色彩：`--theme-primary`、`--theme-primary-bright`、`--theme-primary-deep`、`--theme-accent`、`--theme-accent-deep`、`--theme-ink`、`--theme-ink-soft`、`--theme-slate`、`--theme-muted`、`--theme-canvas`、`--theme-surface`、`--theme-line`、`--theme-success`、`--theme-danger`、`--theme-warn`、`--theme-info`
- 字體：`--theme-font-display`、`--theme-font-body`、`--theme-font-mono`
- 半徑：`--theme-radius-sm`、`--theme-radius`、`--theme-radius-lg`
- 元件行為：`--theme-navbar-bg`、`--theme-navbar-accent-line`、`--theme-btn-press-width`、`--theme-btn-radius`、`--theme-stat-motif`

品牌專屬 tokens（`--scoot-*` / `--eva-*` / `--cal-*` / `--jx-*`）MAY 在對應 data-theme scope 內保留作為映射來源。

#### Scenario: 有效 data-theme 值套用後中性 tokens 可解析
- **WHEN** 頁面 `<html>` 設定 `data-theme="scoot"`、`data-theme="eva"`、`data-theme="china-airlines"` 或 `data-theme="starlux"` 其中之一
- **THEN** 瀏覽器 computed style 於 `:root` SHALL 成功解析所有 `--theme-*` 中性 tokens，且不得有任一 `--theme-*` token 解析為空字串

#### Scenario: 元件 CSS 不引用品牌專屬 tokens
- **WHEN** 開發者檢視 `app/static/css/style.css` 中任一元件規則（`.navbar-theme`、`.btn-theme*`、`.card`、`.card-header-theme`、`.table-theme*`、`.stat-theme*`、`.badge-theme-*`、`.alert`、`.form-control`、`.form-select`、`.form-label`）
- **THEN** 這些規則 MUST 只引用 `var(--theme-*)` 或純 `#ffffff`、`transparent`、`currentColor` 等中性值；不得出現 `var(--scoot-*)`、`var(--eva-*)`、`var(--cal-*)`、`var(--jx-*)`

#### Scenario: 非法 data-theme 值不得造成頁面無樣式
- **WHEN** 頁面 `<html data-theme="nonexistent">`（非四個合法值之一）
- **THEN** 前端 FOUC 防護 script SHALL 於首屏將屬性覆寫為 `scoot`；頁面 MUST 顯示 Scoot 預設主題樣式

### Requirement: 主題切換 UI（navbar 下拉選單）

導航列（`.navbar-theme` 或其 `.navbar-scoot` 別名）SHALL 於右側提供主題切換下拉選單。切換器 MUST 符合以下條件：

- 切換按鈕 MUST 具備 `aria-label="主題切換"`（或等效文字），可鍵盤聚焦。
- 下拉選單 MUST 列出四個主題選項，顯示文字為：「酷航 Scoot」、「長榮航空 EVA Air」、「中華航空 China Airlines」、「星宇航空 Starlux」。
- 每個選項 MUST 為 `<button>` 或 `<a>` 元素，具備 `data-theme-value` 屬性，其值為對應 data-theme 值（`scoot`、`eva`、`china-airlines`、`starlux`）。
- 當前生效的主題選項 MUST 透過 `aria-current="true"` 或等效視覺標示（勾選 icon）呈現為「選中」狀態。
- 切換器 MUST 在所有四個頁面（`/`、`/flights`、`/charts`、`/status`）皆可用。

#### Scenario: 切換器於每個頁面皆可見
- **WHEN** 使用者載入 `/`、`/charts` 或 `/status` 任一頁面
- **THEN** 回應 HTML SHALL 包含主題切換器元素；元素中 MUST 同時出現四個 `data-theme-value="scoot"`、`data-theme-value="eva"`、`data-theme-value="china-airlines"`、`data-theme-value="starlux"` 的選項

#### Scenario: 切換器具備 aria-label
- **WHEN** 開發者檢視 base.html 渲染的切換按鈕
- **THEN** 觸發下拉選單的按鈕 MUST 具備 `aria-label` 屬性，內容為「主題切換」或等效繁體中文描述

#### Scenario: 切換器顯示繁體中文標籤
- **WHEN** 使用者展開主題切換下拉選單
- **THEN** 四個選項 SHALL 顯示繁體中文標籤：「酷航」、「長榮航空」、「中華航空」、「星宇航空」（允許附掛對應英文名）

### Requirement: 主題切換行為與持久化

系統 SHALL 提供 `app/static/js/theme-switcher.js` 實作主題切換行為。JS MUST：

- 於 DOMContentLoaded 後綁定所有 `[data-theme-value]` 選項的 click 事件。
- 點擊時 MUST：
  1. 以 `document.documentElement.setAttribute('data-theme', <value>)` 套用新主題。
  2. 以 `localStorage.setItem('flightprice-theme', <value>)` 持久化。
  3. 於 `document` 上派發 `CustomEvent('themechange', { detail: { theme: <value> } })`。
  4. 將切換器 UI 中原本帶有 `aria-current="true"` 的選項改為非選中，並將新選中的選項加上 `aria-current="true"`。
- 不得整頁重新載入（`window.location.reload` 禁止）。

localStorage key MUST 為 `flightprice-theme`，值為四個合法 data-theme 值之一。

#### Scenario: 點擊選項切換主題（不重載）
- **WHEN** 使用者於下拉選單點擊某主題選項
- **THEN** `document.documentElement` 的 `data-theme` 屬性 SHALL 立即更新為對應值；`localStorage.getItem('flightprice-theme')` SHALL 回傳該值；頁面 MUST 未重新載入（同一 `window` instance）

#### Scenario: 切換事件廣播
- **WHEN** 使用者切換主題
- **THEN** `document` SHALL 派發 `themechange` CustomEvent，且 `event.detail.theme` SHALL 等於新主題值

#### Scenario: JS 原始碼包含關鍵符號
- **WHEN** 開發者檢視 `app/static/js/theme-switcher.js`
- **THEN** 該檔案 MUST 包含字串 `flightprice-theme`、`data-theme-value`、`themechange`；且 MUST 不得出現 `window.location.reload` 或 `location.reload`

### Requirement: 防止主題首屏閃爍（FOUC 防護）

`app/templates/base.html` 的 `<head>` 區塊 SHALL 於所有 `<link rel="stylesheet">` 之前（即 Bootstrap 與 style.css 載入前）嵌入 inline script。該 script MUST：

- 嘗試讀取 `localStorage.getItem('flightprice-theme')`。
- 驗證值是否為 `scoot`、`eva`、`china-airlines`、`starlux` 四者之一。
- 合法則設為 `<html>` 的 `data-theme` 屬性；否則（包含 null、非法值、localStorage 不可用）設為 `scoot`。
- MUST 以 try/catch 包覆 localStorage 存取以防瀏覽器隱私模式例外。

#### Scenario: base.html 首屏 script 存在
- **WHEN** 開發者檢視 `app/templates/base.html`
- **THEN** `<head>` 區段 SHALL 於 `<link href=".*/bootstrap.*\.css">` 與 `<link href="{{ url_for('static', filename='css/style.css') }}">` 之前出現 inline `<script>`；該 script MUST 包含字串 `flightprice-theme`、`data-theme` 與 `try`

#### Scenario: localStorage 不可用時回退預設
- **WHEN** 瀏覽器 localStorage 拋出例外（例：私密模式禁用）
- **THEN** inline script MUST 捕獲例外並將 `<html data-theme>` 設為 `scoot`；頁面 SHALL 顯示 Scoot 主題

### Requirement: Chart.js 動態讀取主題色彩

`app/templates/charts.html` 中的 Chart.js 配置 SHALL：

- 所有線條色、資料點色、tooltip 色、grid 色、刻度色、legend 色 MUST 透過 `getComputedStyle(document.documentElement).getPropertyValue('--theme-<token>').trim()` 動態取得，不得硬編色碼（允許例外：純 `transparent`、`#ffffff` 等中性值）。
- MUST 註冊 `document.addEventListener('themechange', ...)` 監聽器；主題切換時 MUST 重新計算上述色彩並呼叫 `chart.update()`（或等效重繪方法）。

#### Scenario: Chart.js 源碼以 getPropertyValue 取色
- **WHEN** 開發者檢視 `app/templates/charts.html`
- **THEN** 其內嵌 `<script>` SHALL 包含字串 `getPropertyValue('--theme-` 與 `themechange`；MUST 不得出現硬編十六進位色碼（例：`'#0E0E10'`、`'#FFDA00'`）作為 Chart.js datasets 或 scales 的色彩值

#### Scenario: 主題切換後圖表重繪
- **WHEN** 使用者於 `/charts?flight_id=<id>` 頁面切換主題
- **THEN** `themechange` event 觸發後，Chart.js 實例 SHALL 呼叫 `chart.update()`，且新繪製的線條色 MUST 對應新主題的 `--theme-ink`

### Requirement: 向下相容（scoot 別名 class）

為維持既有測試與模板不變，所有原先以 `.*-scoot` 命名的 class SHALL 保留為中性 class 的別名。具體別名對應如下（CSS 規則 MUST 以 selector 群組方式實作，使 `.*-theme*` 與 `.*-scoot*` 套用同一組 declaration）：

| 別名 class（保留） | 中性 class（新增） |
|--------------------|---------------------|
| `.navbar-scoot` | `.navbar-theme` |
| `.btn-scoot` | `.btn-theme` |
| `.btn-scoot-secondary` | `.btn-theme-secondary` |
| `.btn-scoot-danger` | `.btn-theme-danger` |
| `.btn-scoot-success` | `.btn-theme-success` |
| `.btn-scoot-warning` | `.btn-theme-warning` |
| `.card-header-scoot` | `.card-header-theme` |
| `.table-scoot-wrap` | `.table-theme-wrap` |
| `.table-scoot` | `.table-theme` |
| `.stat-scoot` | `.stat-theme` |
| `.stat-scoot--ink` | `.stat-theme--ink` |
| `.stat-scoot--yellow` | `.stat-theme--primary` |
| `.stat-scoot--success` | `.stat-theme--success` |
| `.stat-scoot--danger` | `.stat-theme--danger` |
| `.stat-scoot--slate` | `.stat-theme--slate` |
| `.badge-scoot-success` | `.badge-theme-success` |
| `.badge-scoot-danger` | `.badge-theme-danger` |
| `.badge-scoot-muted` | `.badge-theme-muted` |

#### Scenario: 既有 class 在所有主題下仍渲染對應樣式
- **WHEN** 任一主題啟用（`data-theme="scoot"|"eva"|"china-airlines"|"starlux"`），且頁面中出現 `.navbar-scoot`、`.btn-scoot`、`.btn-scoot-danger`、`.table-scoot`、`.badge-scoot-success`、`.stat-scoot--ink` 等舊 class
- **THEN** 這些元素 SHALL 套用與同主題下對應中性 class（`.navbar-theme`、`.btn-theme`、`.btn-theme-danger` …）完全相同的 computed style

#### Scenario: 現有模板 class 字串不必改動即可通過既有測試
- **WHEN** 於預設 data-theme="scoot" 下執行 `tests/test_theme_smoke.py` 中所有 pre-existing Scoot 相關測試
- **THEN** 所有斷言 SHALL 通過；`.navbar-scoot`、`.btn-scoot`、`.btn-scoot-danger`、`.table-scoot`、`.badge-scoot-success`、`.stat-scoot--ink`、`.stat-scoot--success`、`.stat-scoot--danger` 等字串 MUST 仍於 HTML 或 CSS 中出現

### Requirement: 主題切換可及性

主題切換功能 SHALL 符合 WCAG 2.1 AA 對應指引：

- 切換按鈕與下拉選項 MUST 可以 Tab 鍵聚焦、Enter／Space 觸發。
- 焦點樣式 MUST 符合現有 `:focus-visible` 規範（至少 `2px` 外描邊、與背景對比 ≥ 3:1）。
- 非啟用選項與啟用選項 MUST 同時以視覺（勾選 icon）與 ARIA（`aria-current="true"`）區分，不得僅靠顏色。
- 切換動作 MUST 不依賴滑鼠懸浮開啟選單；點擊按鈕即開。
- `prefers-reduced-motion: reduce` 下切換後 MUST 不觸發任何額外動畫（直接替換屬性值）。

#### Scenario: 鍵盤操作完整切換
- **WHEN** 使用者以 Tab 聚焦切換按鈕並按 Enter 開啟選單，再以方向鍵或 Tab 移到某選項並按 Enter
- **THEN** `<html data-theme>` SHALL 切換為該選項值；焦點 MUST 保持於切換器區域（不得跳回頁首）

#### Scenario: 狀態不單靠顏色
- **WHEN** 使用者檢視下拉選單中「當前主題」的視覺標示
- **THEN** 該選項 MUST 同時具備 `aria-current="true"` 與可視覺辨識的文字或 icon（例：`✓`、`(使用中)`），不得僅以字體色／底色差異呈現選中狀態
