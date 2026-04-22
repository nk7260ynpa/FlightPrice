### Requirement: 星宇航空品牌色彩 Tokens

系統 SHALL 於 `app/static/css/style.css` 的 `:root[data-theme="starlux"]` scope 中定義星宇航空品牌 CSS 自訂屬性色彩 tokens，並將中性語意 tokens（`--theme-*`）映射至對應品牌 token。色碼如下（允許 ±1% 明度微調，不得改變色相）：

品牌原生 tokens：

- `--jx-primary: #0E1842`（午夜藍 Midnight Navy，主色）
- `--jx-primary-bright: #1A2C5A`（hover，僅微亮）
- `--jx-primary-deep: #070D25`（極深層按壓）
- `--jx-accent: #C8A96A`（香檳金 Champagne Gold）
- `--jx-accent-bright: #D9BC7E`（金色 hover）
- `--jx-accent-deep: #A68848`（金色分隔 / 按壓）
- `--jx-ink: #111520`（主文字）
- `--jx-ink-soft: #252A3A`
- `--jx-slate: #5A6078`
- `--jx-muted: #9095A8`
- `--jx-canvas: #F4F1EA`（香檳米白，偏暖）
- `--jx-surface: #FBF8F1`（象牙紙本感）
- `--jx-line: #E3DDCC`（淺金線）
- `--jx-success: #6B8E5A`（克制綠，非亮綠）
- `--jx-danger: #8C2E2A`（暗酒紅，非亮紅）
- `--jx-warn: #B8893A`（暗金橘）
- `--jx-info: #3A5B8A`（沉穩藍）

中性 tokens 映射：於同一 scope 內將 `--theme-*` 各項（`--theme-primary`、`--theme-primary-bright`、`--theme-primary-deep`、`--theme-accent`、`--theme-accent-deep`、`--theme-ink`、`--theme-ink-soft`、`--theme-slate`、`--theme-muted`、`--theme-canvas`、`--theme-surface`、`--theme-line`、`--theme-success`、`--theme-danger`、`--theme-warn`、`--theme-info`）設為對應 `var(--jx-*)`。

#### Scenario: 星宇色彩 tokens 可解析
- **WHEN** 使用者瀏覽任一頁面且 `<html data-theme="starlux">`
- **THEN** 瀏覽器 computed style SHALL 解析 17 項 `--jx-*` token（含 accent-bright）與 16 項 `--theme-*` 色彩 token，色碼對應本 Requirement 定義

#### Scenario: 星宇 CSS 規則存在於 style.css
- **WHEN** 開發者檢視 `app/static/css/style.css`
- **THEN** 檔案 MUST 包含 `:root[data-theme="starlux"]` selector，且該 block 內 MUST 出現字串 `#0E1842` 與 `#C8A96A`

### Requirement: 星宇字體堆疊

`:root[data-theme="starlux"]` scope MUST 設定：

- `--theme-font-display`：起首 `"Cormorant Garamond"`，fallback 依序 `"EB Garamond"`、`"Noto Serif TC"`、`"Playfair Display"`、`serif`（editorial serif）
- `--theme-font-body`：起首 `"Inter Tight"`，fallback 依序 `"Noto Sans TC"`、`"PingFang TC"`、`-apple-system`、`BlinkMacSystemFont`、`sans-serif`
- `--theme-font-mono`：起首 `"JetBrains Mono"`，fallback 依序 `ui-monospace`、`monospace`

`app/templates/base.html` 的 Google Fonts `<link>` MUST 載入 `Cormorant Garamond` 與 `Inter Tight` 字型 family（可與其他主題字型合併於單一 URL）。

#### Scenario: 星宇主題 body 字體
- **WHEN** `<html data-theme="starlux">` 載入完成
- **THEN** `<body>` computed `font-family` SHALL 以 `Inter Tight` 開頭

#### Scenario: 星宇主題 display 字體
- **WHEN** `<html data-theme="starlux">` 下頁面出現 `<h2>`
- **THEN** 該元素 computed `font-family` SHALL 以 `Cormorant Garamond` 開頭

### Requirement: 星宇 Navbar 視覺

`<html data-theme="starlux">` 下 `.navbar-theme`（或其別名 `.navbar-scoot`）SHALL：

- 背景 `var(--theme-primary)`（即 `#0E1842` 午夜藍）實底
- 底部裝飾線 `1px solid var(--theme-accent)`（香檳金髮絲線，emphasis 細節而非粗邊）
- 導航品牌文字 MUST 為 `var(--theme-accent)` 金色、使用 `--theme-font-display`（襯線字）、字重 ≥ 600、`letter-spacing` ≥ `0.1em`
- 導航連結（`.nav-link`）MUST 為 `#FFFFFF` 白色或 `var(--theme-accent)` 金色，active 狀態 MUST 以「底部 `1px solid var(--theme-accent)` 金色下劃線」指示，**不使用**實底 pill（保持編輯風格留白感）

#### Scenario: 星宇 Navbar 顯示
- **WHEN** 使用者於 `data-theme="starlux"` 下瀏覽任一頁面
- **THEN** 頂部 navbar 背景 SHALL 為午夜藍 `#0E1842`、底部 SHALL 為 1px 香檳金髮絲線；品牌文字 MUST 為襯線字體的金色文字

#### Scenario: 星宇 navbar active 狀態（金色下劃線）
- **WHEN** 使用者位於 `/flights`、`/charts`、`/status` 且 `data-theme="starlux"`
- **THEN** 對應 `.nav-link.active` MUST 呈現透明底 + 底部 `1px` 或 `2px solid var(--theme-accent)` 金色下劃線；MUST 不套用實色 pill 背景

### Requirement: 星宇按鈕樣式差異化

`<html data-theme="starlux">` 下按鈕 SHALL 與其他三主題採不同視覺語言：

- `--theme-btn-press-width: 0px`（廢除 3px 粗底邊按壓）
- `--theme-btn-radius: 4px`（editorial 方正感，其他三主題為 10px）
- 主按鈕（`.btn-theme` / `.btn-scoot`）背景 `var(--theme-primary)` 午夜藍、文字 `var(--theme-accent)` 香檳金、`1px solid var(--theme-accent)` 金色細邊
- 主按鈕 hover：背景 `var(--theme-primary-bright)` 或 `var(--theme-accent)` 香檳金底 + 午夜藍文字（互換品牌色）
- 主按鈕 `:active`：MUST 使用 `box-shadow: inset 0 1px 2px rgba(0,0,0,0.2)` 模擬微凹（`prefers-reduced-motion` 下 MUST 停用）；MAY 搭配 `transform: translateY(0.5px)`
- 次按鈕（`.btn-theme-secondary`）透明底 + `1px solid var(--theme-accent)` + 文字 `var(--theme-accent)`
- 危險按鈕（`.btn-theme-danger`）背景 `var(--theme-danger)` `#8C2E2A`（暗酒紅，非亮紅）、文字 `#FFFFFF`

#### Scenario: 星宇主按鈕樣式
- **WHEN** `<html data-theme="starlux">` 下頁面出現主操作按鈕
- **THEN** 按鈕 SHALL 顯示午夜藍 `#0E1842` 背景、香檳金 `#C8A96A` 文字、`4px` 圓角、`1px solid` 金色細邊；MUST 不顯示 3px 粗底按壓邊

#### Scenario: 星宇按鈕按壓回饋（box-shadow inset）
- **WHEN** 使用者於 `data-theme="starlux"` 點擊主按鈕處於 `:active` 狀態且 `prefers-reduced-motion` 非 `reduce`
- **THEN** 按鈕 MUST 套用 `box-shadow: inset` 微凹效果；`prefers-reduced-motion: reduce` 下 MUST 不套用任何 transform 與 box-shadow 動態

### Requirement: 星宇統計卡與表格配色

`<html data-theme="starlux">` 下的統計卡與表格 SHALL 維持精品 editorial 視覺語言，元件規則 MUST 符合下列條件：

- `--theme-stat-motif`：以 inline SVG data URI 表達半透明 `var(--theme-accent)` 色的 6 pt 星形圖案（對應「星宇」名稱），尺寸約 12px；位於統計卡右下角 `::after`
- 表格 `.table-theme` 表頭 MUST 為 `var(--theme-primary)` 午夜藍底、`var(--theme-accent)` 香檳金字（使用 `--theme-font-display` 襯線字體）
- 表身偶數列 MUST 為 `var(--theme-accent)` 6% alpha 極淡金底（不得太亮影響 editorial 感）
- 卡片（`.card`）背景 `var(--theme-surface)`（`#FBF8F1` 象牙紙本感），不得為純白
- 卡片邊框 MUST 為 `1px solid var(--theme-line)` 淺金線

#### Scenario: 星宇統計卡星形裝飾
- **WHEN** `<html data-theme="starlux">` 下頁面渲染 `.stat-theme`（或 `.stat-scoot`）
- **THEN** 卡片右下角 `::after` 偽元素 MUST 出現金色星形裝飾（`--theme-stat-motif` 引用 SVG data URI）

#### Scenario: 星宇表格表頭襯線金字
- **WHEN** `<html data-theme="starlux">` 下載入 `.table-theme` 資料表
- **THEN** 表頭 `thead th` SHALL 為午夜藍底、香檳金字，字體 `font-family` SHALL 以 `Cormorant Garamond` 開頭

### Requirement: 星宇主題 AA 對比底線

`<html data-theme="starlux">` 下所有文字 SHALL 符合 WCAG 2.1 AA：

- 午夜藍 `#0E1842` 底 + 白字對比 ≥ 13:1（AAA 過關）
- 午夜藍底 + 香檳金 `#C8A96A` 字對比 ≥ 6:1（AA 過關）
- 香檳金 `#C8A96A` 底 MUST 僅搭配 `var(--theme-ink)`（`#111520`）深色文字；禁止白字。
- `.badge-theme-success`（success 6B8E5A）若作為背景色，文字 MUST 為 `#FFFFFF`；作為文字色（於淡底 pill 上）MUST 搭配該色 12% alpha 底，確保文字對比 ≥ 4.5:1。
- `.badge-theme-warn` / warning 相關元件不得使用白字於 `#B8893A` 底（對比約 3.6:1，僅 AA large 過關）；MUST 改為使用 `var(--theme-ink)` 深色文字或提高背景透明度呈現。
- `prefers-reduced-motion: reduce` 下按鈕 box-shadow inset 動態、transform、hover transition MUST 停用或動畫時間 ≤ 0.01ms。

#### Scenario: 星宇金底禁白字
- **WHEN** 開發者檢視任何使用 `var(--theme-accent)`（香檳金）為背景的元件（按鈕 hover、badge、statcard accent 變體）
- **THEN** 其文字 MUST 為 `var(--theme-ink)` 或等效深色，不得為 `#ffffff`、`white` 或白色等效色

#### Scenario: 星宇 warn 對比
- **WHEN** 開發者檢視 `.badge-theme-warn` 或任何 warning 語意元件於 `data-theme="starlux"` 下樣式
- **THEN** 若背景為 `#B8893A` 暗金橘，文字 MUST 為 `var(--theme-ink)` 或 `#111520` 深色；MUST 不得為白色
